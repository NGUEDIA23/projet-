# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from tokenizers import Tokenizer
from .models import Article
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import activate
from transformers import GPT2LMHeadModel, GPT2Tokenizer


def article_list(request):
    articles = Article.objects.all()
    return render(request, 'main/article_list.html', {'articles': articles})

def home(request):
    return redirect('article_list')

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'main/article_detail.html', {'article': article})
def change_language(request):
    language = request.GET.get('language', 'en')
    activate(language)
    response = redirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie('django_language', language)
    return response


# Charger le modèle GPT-2 et le tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

def chatbot(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        chat_history = request.session.get('chat_history', '')

        # Ajouter l'entrée utilisateur à l'historique du chat
        if chat_history:
            chat_history += f"\nUser: {user_input}\nBot:"
        else:
            chat_history = f"User: {user_input}\nBot:"

        # Générer la réponse du bot
        input_ids = tokenizer.encode(chat_history + user_input, return_tensors='pt')
        bot_response = model.generate(input_ids, max_length=100, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
        bot_response_text = tokenizer.decode(bot_response[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
         
        # Mettre à jour l'historique du chat dans la session
        request.session['chat_history'] = chat_history + bot_response_text

        return render(request, 'chatbot.html', {'response': bot_response_text, 'user_input': user_input})
     
    return render(request, 'chatbot.html')
   # Charger le modèle RAG
    retriever = RagRetriever.from_pretrained("facebook/rag-token-nq")
    model = RagTokenForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)

    # Utiliser le modèle pour générer des réponses
    input_dict = tokenizer.prepare_seq2seq_batch("What is the capital of France?", return_tensors='pt')
    generated = model.generate(input_dict['input_ids'], num_return_sequences=1)
    print(tokenizer.batch_decode(generated, skip_special_tokens=True))

# Charger le tokenizer et le modèle RAG
from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration

# Initialisation des composants RAG (exemples, adaptez selon votre modèle spécifique)
tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-base")
retriever = RagRetriever.from_pretrained("facebook/rag-token-base", index_name="exact")
generator = RagTokenForGeneration.from_pretrained("facebook/rag-token-base")

def search_with_rag(request):
    query = request.GET.get('q', '')

    if query:
        try:
            # Charger le RagRetriever en autorisant le code distant
            retriever = RagRetriever.from_pretrained("facebook/rag-token-base", index_name="exact", trust_remote_code=True)
            
            # Effectuer la recherche augmentée avec RAG
            input_dict = tokenizer(query, return_tensors="pt")
            retrieved_docs = retriever(input_dict['input_ids'], return_tensors="pt")
            generated = generator.generate(retrieved_docs['context_input_ids'], num_return_sequences=1)

            # Décoder la réponse générée
            answers = tokenizer.batch_decode(generated, skip_special_tokens=True)

            context = {
                'query': query,
                'answers': answers,
            }
            return render(request, 'search_results.html', context)
        except Exception as e:
            
            # Gérer les erreurs d'initialisation du retriever
            return HttpResponse(f"Erreur lors de l'initialisation du retriever : {e}")
    else:
        return render(request, 'search_form.html')
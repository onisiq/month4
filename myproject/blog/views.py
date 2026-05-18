from django.contrib.auth import login
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView

from .forms import CategoryForm, PostForm, RegisterForm
from .models import Category, Post


# Страница регистрации.
# FormView нужен, когда мы работаем с обычной формой, а не напрямую с моделью.
class RegisterView(FormView):
    # Какой HTML-шаблон открыть.
    template_name = 'blog/register.html'
    # Какую форму показать на странице.
    form_class = RegisterForm
    # Куда перейти, если регистрация прошла успешно.
    # reverse_lazy используем в классах, чтобы URL искался не сразу, а когда понадобится.
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        # Если форма правильная, сохраняем нового пользователя.
        user = form.save()
        # Сразу делаем вход после регистрации.
        login(self.request, user)
        # Дальше Django сам отправит пользователя на success_url.
        return super().form_valid(form)


# Страница создания категории.
# CreateView сам показывает форму и сохраняет объект в базу.
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category_form.html'
    success_url = reverse_lazy('post_list')

    def get_next_url(self):
        # Смотрим, откуда пришел пользователь.
        # Например, если пришел со страницы создания поста, там будет next=post_create.
        return self.request.POST.get('next') or self.request.GET.get('next')

    def get_context_data(self, **kwargs):
        # Берем обычный context от Django.
        context = super().get_context_data(**kwargs)
        # Добавляем next_url в шаблон, чтобы шаблон знал, куда потом вернуться.
        context['next_url'] = self.get_next_url()
        return context

    def get_success_url(self):
        # Если категорию создавали во время создания поста,
        # возвращаем пользователя обратно на создание поста.
        if self.get_next_url() == 'post_create':
            return reverse('post_create')
        return super().get_success_url()


# Страница создания поста.
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        # self.object - это пост, который только что создали.
        # После создания открываем страницу именно этого поста.
        return reverse('post_detail', kwargs={'pk': self.object.pk})


# Страница одного поста.
# DetailView сам ищет объект по pk из URL.
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    # В шаблоне объект будет называться post.
    context_object_name = 'post'


# Страница удаления поста.
# DeleteView сначала показывает подтверждение, а после POST удаляет объект.
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    context_object_name = 'post'
    # После удаления возвращаемся к списку постов.
    success_url = reverse_lazy('post_list')


# Страница со списком постов.
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    # В шаблоне список будет называться posts.
    context_object_name = 'posts'

    def get_queryset(self):
        # Показываем только опубликованные посты с рейтингом 5 или выше.
        # select_related('category') заранее подтягивает категорию, чтобы было меньше запросов к базе.
        return Post.objects.select_related('category').filter(is_published=True, rate__gte=5)

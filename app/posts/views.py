from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Post
from .forms import PostCreateForm


def post_list(request):
    # 1. Post모델에
    #  created_at (생성시간 저장)
    #  modified_at (수정시간 적용)
    #   두 필드를 추가

    # 2. Post모델이 기본적으로 pk내림차순으로 정렬되도록 설정

    # 3. 모든 Post객체에 대한 QuerySet을
    #    render의 context인수로 전달 (키: posts)

    # 4. posts/post_list.html을 Template으로 사용
    #     템플릿에서는 posts값을 순회하며
    #     각 Post의 photo정보를 출력

    # 5. url은 posts.urls모듈을 사용
    #    config.urls에서 해당 모듈을 include
    #    posts.urls.app_name = 'posts'를 사용
    #     include할 URL은 'posts/'
    #     view의 URL은 비워둔다
    #      결과:localhost:8000/posts/ 로 접근시
    #            이 view가 처리하도록 함
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'posts/post_list.html', context)


def post_create(request):
    # 이 view로 왔는데
    # User가 로그인 된 상태가 아니면
    #  is_authenticated <- 검색
    # posts:post-list로 보내버리기
    if not request.user.is_authenticated:
        return redirect('posts:post-list')

    if request.method == 'POST':
        # request.FILES에 form에서 보낸 파일 객체가 들어있음
        # 새로운 post를 생성한다.
        # author는 User.objects.first()
        # photo는 request.FILES에 있는 내용을 적절히 꺼내서 쓴다
        # 완료된 후 posts:post-list로 redirect
        post = Post(
            # SessionMiddleware
            # AuthenticationMiddleware
            #  를 통해서 request의 user속성에
            #  해당 사용자 인스턴스가 할당
            author=request.user,
            photo=request.FILES['photo'],
        )
        post.save()
        return redirect('posts:post-list')
    else:
        # GET요청의 경우, 빈 Form인스턴스를 context에 담아서 전달
        # Template에서는 'form'키로 해당 Form인스턴스 속성을 사용 가능
        form = PostCreateForm()
        context = {
            'form': form,
        }
        return render(request, 'posts/post_create.html', context)
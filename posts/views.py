import json

from django.views import View
from django.http import JsonResponse
from .models import Post
from users.auth_decorator import user_auth


class PostView(View):
    @user_auth
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user

            post = Post.objects.create(
                title = data['title'],
                author = user.username,
                content = data['content'],
                user = user
            )

            data = {
                "title" : post.title,
                "author" : post.author,
                "content" : post.content,
                "created_at" : post.created_at,
                "updated_at" : post.updated_at
            }

            return JsonResponse({'message' : 'CREATED', 'data' : data}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    def get(self, request, post_id):
        try:
            if not Post.objects.filter(id = post_id).exists():
                return JsonResponse({'message' : 'DOES NOT EXIST'}, status = 404)
            print(post_id)
            post = Post.objects.get(id = post_id)
            print(post)
            data = {
                "title": post.title,
                "author": post.author,
                "content": post.content,
                "created_at": post.created_at,
                "updated_at": post.updated_at
            }

            return JsonResponse({'data' : data}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    @user_auth
    def patch(self, request, post_id):
        try:
            data = json.loads(request.body)

            if not Post.objects.filter(id = post_id).exists():
                return JsonResponse({'message' : 'DOES NOT EXIST'}, status = 404)

            print('==================================')
            print(Post.objects.get(id = post_id).user)
            print('==================================')

            if Post.objects.get(id = post_id).user == request.user:
                return JsonResponse({'message' : 'UNAUTHORIZED USER'}, status = 400)

            post = Post.objects.filter(id = post_id, user = request.user)
            post.update(content = data['content'])

            return JsonResponse({'message' : 'UPDATED SUCCESSFULLY'}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    @user_auth
    def delete(self, request, post_id):
        if not Post.objects.filter(id = post_id).exists():
            return JsonResponse({'message': 'DOES NOT EXIST'}, status=404)

        if Post.objects.get(id = post_id).user == request.user:
            return JsonResponse({'message': 'UNAUTHORIZED USER'}, status=400)

        Post.objects.get(id = post_id).delete()

        return JsonResponse({'message' : 'POST DELETED'}, status = 200)


class PostlistView(View):
    def get(self, request):
        limit = int(request.GET.get("limit", 5))
        offset = int(request.GET.get("offset", 0))
        posts = Post.objects.all()

        data = [{
            "username": post.user.username,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at
        } for post in posts]

        data = data[offset:offset + limit]
        count = len(data)

        return JsonResponse({"count": count, "data": data}, status = 200)
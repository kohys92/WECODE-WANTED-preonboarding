import json
import jwt

from django.test import TestCase, Client
from my_settings import ALGORITHM
from .models import Post
from users.models import User
from noticeboard.settings import SECRET_KEY


class PostViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            id=1,
            username='test1',
            email='test@gmail.com',
            password='Aaaa123@'
        )

        User.objects.create(
            id=2,
            username='test2',
            email='test2@gmail.com',
            password='Aaaa123@'
        )

        Post.objects.bulk_create([
            Post(
                id=1,
                title = 'test_post1',
                author = User.objects.get(id=1).username,
                content = 'test_content1',
                user = User.objects.get(id=1)
            ),
            Post(
                id=2,
                title='test_post2',
                author=User.objects.get(id=1).username,
                content='test_content2',
                user=User.objects.get(id=1)
            ),
            Post(
                id=3,
                title = 'test_post3',
                author = User.objects.get(id=1).username,
                content = 'test_content3',
                user = User.objects.get(id=1)
            ),
            Post(
                id=4,
                title='test_post4',
                author=User.objects.get(id=2).username,
                content='test_content4',
                user=User.objects.get(id=2)
            ),
            Post(
                id=5,
                title='test_post5',
                author=User.objects.get(id=2).username,
                content='test_content5',
                user=User.objects.get(id=2)
            ),
            Post(
                id=6,
                title='test_post6',
                author=User.objects.get(id=2).username,
                content='test_content6',
                user=User.objects.get(id=2)
            ),
            Post(
                id=7,
                title='test_post7',
                author=User.objects.get(id=2).username,
                content='test_content7',
                user=User.objects.get(id=2)
            )
            ])

    def tearDown(self):
        Post.objects.all().delete()
        User.objects.all().delete()

    def test_post_view_post_create_success(self):
        client = Client()

        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm = ALGORITHM)
        header = {'HTTP_Authorization' : access_token}
        post = {
            'title' : 'test_post',
            'author' : User.objects.get(id=1).username,
            'content' : 'test_content'
        }

        response = client.post('/posts', json.dumps(post), **header, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_post_view_post_key_error(self):
        client = Client()

        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm=ALGORITHM)
        header = {'HTTP_Authorization': access_token}

        post = {
            'titleeeeee': 'test_post',
            'author': User.objects.get(id=1).username,
            'content': 'test_content'
        }

        response = client.post('/posts', json.dumps(post), **header, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_get_success(self):
        client = Client()
        response = client.get('/posts/2')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "data" : {
                "title" : "test_post2",
                "author" : User.objects.get(id=1).username,
                "content" : "test_content2",
                "created_at" : Post.objects.get(id=1).created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at" : Post.objects.get(id=1).updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
        
    def test_post_get_does_not_exist(self):
        client = Client()
        response = client.get('/posts/81283928')
        
        self.assertEqual(response.status_code, 404)
    
    def test_post_view_patch_success(self):
        client = Client()

        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm=ALGORITHM)
        header = {'HTTP_Authorization': access_token}

        response = client.patch('/posts/5', json.dumps({'content' : 'updated content test'}), 
                                **header, content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'UPDATED SUCCESSFULLY'})
    
    def test_patch_post_does_not_exist(self):
        client = Client()

        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm=ALGORITHM)
        header = {'HTTP_Authorization': access_token}

        response = client.patch('/posts/123124', json.dumps({'content': 'Test patch update'}),
                                **header, content_type='application/json')

        self.assertEquals(response.status_code, 404)
        
    def test_patch_post_unauthorized_user(self):
        client = Client()

        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm=ALGORITHM)
        header = {'HTTP_Authorization': access_token}
        
        response = client.patch('/posts/1', json.dumps({'content' : 'Test patch unauthorized user'}),
                                **header, content_type='application/json')
        
        self.assertEquals(response.status_code, 400)
        
    def test_patch_post_key_error(self):
        client = Client()

        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm=ALGORITHM)
        header = {'HTTP_Authorization': access_token}

        response = client.patch('/posts/5', json.dumps({'content-keyerror' : 'updated content test'}), 
                                **header, content_type = 'application/json')

        self.assertEquals(response.status_code, 400)
        
    def test_delete_post_success(self):
        client = Client()

        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm=ALGORITHM)
        header = {'HTTP_Authorization': access_token}

        response = client.delete('/posts/5', **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'POST DELETED'})
        
    def test_delete_post_does_not_exist(self):
        client = Client()

        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm=ALGORITHM)
        header = {'HTTP_Authorization': access_token}

        response = client.delete('/posts/55', **header)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message': 'DOES NOT EXIST'})
        
    def test_delete_post_unauthorized_user(self):
        client = Client()

        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm=ALGORITHM)
        header = {'HTTP_Authorization': access_token}

        response = client.delete('/posts/1', **header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'UNAUTHORIZED USER'})
        
    def test_get_post_list_success(self):
        client = Client()
        
        response = client.get('/posts/list')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'count': 3,
                          'data': [
                              {
                                  'title': 'test_post1',
                                  'author': 'test1',
                                  'content': 'test_content1',
                                  'created_at': Post.objects.get(title='test_post1').created_at.strftime('%Y-%m-%d %H:%M:%S'),
                                  'updated_at': Post.objects.get(title='test_post1').updated_at.strftime('%Y-%m-%d %H:%M:%S')
                              },
                              {
                                  'title': 'test_post2',
                                  'author': 'test1', 
                                  'content':'test_content2',
                                  'created_at': Post.objects.get(title='test_post2').created_at.strftime('%Y-%m-%d %H:%M:%S'),
                                  'updated_at': Post.objects.get(title='test_post2').updated_at.strftime('%Y-%m-%d %H:%M:%S')
                              },
                              {
                                  'title': 'test_post3',
                                  'author': 'test1',
                                  'content': 'test_content3',
                                  'created_at': Post.objects.get(title='test_post3').created_at.strftime('%Y-%m-%d %H:%M:%S'),
                                  'updated_at': Post.objects.get(title='test_post3').updated_at.strftime('%Y-%m-%d %H:%M:%S')
                              }
                          ]})



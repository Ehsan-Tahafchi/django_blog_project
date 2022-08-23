from django.test import TestCase
from .models import Post
from django.contrib.auth.models import User
from django.shortcuts import reverse


class BlogPostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="ehsan1")
        cls.post1 = Post.objects.create(
            title="post 5",
            text="this is a post 5",
            author=cls.user,
            status=Post.STATUS_CHOICES[0][0],
        )
        cls.post2 = Post.objects.create(
            title='post 6',
            text='this is a post 6',
            author=cls.user,
            status=Post.STATUS_CHOICES[1][0],
        )

    def test_post_model_str(self):
        post = self.post1
        self.assertEqual(str(post), post.title)

    def test_post_detail(self):
        self.assertEqual(self.post1.title, 'post 5')
        self.assertEqual(self.post1.text, 'this is a post 5')

    def test_post_blog_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_post_blog_by_name(self):
        response = self.client.get(reverse("posts_list_view"))

    def test_post_title_blog_list(self):
        response = self.client.get(reverse("posts_list_view"))
        self.assertContains(response, self.post1.title)

    def test_post_details_blog_on_detail_page(self):
        response = self.client.get(f'/blog/{self.post1.id}/')
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)

    def test_post_detail_url(self):
        response = self.client.get(f'/blog/{self.post1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url_name(self):
        response = self.client.get(reverse('posts_detail_view', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_404(self):
        response = self.client.get(reverse('posts_detail_view', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_draft_post_not_show(self):
        response = self.client.get(reverse("posts_list_view"))
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)

    def test_post_create_view(self):
        response = self.client.post(reverse('post_create_view'), {
            'title': 'test post',
            'text': 'text post',
            'author': self.user.id,
            'status': 'Published',

        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'test post')
        self.assertEqual(Post.objects.last().text, 'text post')

    def test_post_update_view(self):
        response = self.client.post(reverse('post_update_view', args=[self.post2.id]), {
            'title': "post 6 update",
            'text': "this is a post 6 update",
            'author': self.post2.author.id,
            'status': 'Published'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'post 6 update')
        self.assertEqual(Post.objects.last().text, 'this is a post 6 update')

    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete_view', args=[self.post2.id]))
        self.assertEqual(response.status_code, 302)

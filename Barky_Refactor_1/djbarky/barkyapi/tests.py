from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework import routers
from rest_framework.test import APIRequestFactory, APITestCase, APIClient #import APIClient

from .models import Bookmark, Snippet #import new class(Snippet)
from .views import BookmarkViewSet
from django.contrib.auth.models import User #new

# Create your tests here.
# test plan


class BookmarkTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.bookmark = Bookmark.objects.create(
            id=1,
            title="Awesome Django",
            url="https://awesomedjango.org/",
            notes="Best place on the web for Django.",
        ) #attributes showed in Bookmark Instance page

        self.bookmark2 = Bookmark.objects.create(
            id=2,
            title="Google",
            url="https://google.com/",
            notes="Google Home Page.",
        )
        # print(f"bookmark id: {self.bookmark.id}")

        # the simple router provides the name 'bookmark-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:bookmark-list")
        self.detail_url = reverse(
            "barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id}
        )

    # 1. create a bookmark
    def test_create_bookmark(self):
        """
        Ensure we can create a new bookmark object.
        """

        # the full record is required for the POST
        data = {
            "id": 99,
            "title": "Django REST framework",
            "url": "https://www.django-rest-framework.org/",
            "notes": "Best place on the web for Django REST framework.",
        }
        response = self.client.post(self.list_url, data, format="json")
        # print("Test Create Bookmark")
        # print(response.data)
        # print(response.status_code)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Bookmark.objects.count(), 3)
        self.assertEqual(Bookmark.objects.get(id=99).title, "Django REST framework")

    # 2. list bookmarks
    def test_list_bookmarks(self):
        """
        Ensure we can list all bookmark objects.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"][0]["title"], self.bookmark.title)

    # 3. retrieve a bookmark
    def test_retrieve_bookmark(self):
        """
        Ensure we can retrieve a bookmark object.
        """
        response = self.client.get(self.detail_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], self.bookmark.title)

    # 4. delete a bookmark
    def test_delete_bookmark(self):
        """
        Ensure we can delete a bookmark object.
        """
        response = self.client.delete(
            reverse("barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bookmark.objects.count(), 1)

    # 5. update a bookmark
    def test_update_bookmark(self):
        """
        Ensure we can update a bookmark object.
        """
        # the full record is required for the POST
        data = {
            "id": 99,
            "title": "Awesomer Django",
            "url": "https://awesomedjango.org/",
            "notes": "Best place on the web for Django just got better.",
        }
        response = self.client.put(
            reverse("barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id}),
            data,
            format="json",
        )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], "Awesomer Django")
    
    # 20. list bookmarks by date
    def test_ordering_by_date_ascending(self):

        url = reverse('barkyapi:bookmark-list') + '?ordering=date_added'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['date_added'])
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)

    def test_ordering_by_date_descending(self):
        url = reverse('barkyapi:bookmark-list') + '?ordering=-date_added'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['date_added'], reverse=True)
        # print(response_result)
        # print(expected_result)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)
    
    # 23. list bookmarks by title
    def test_ordering_by_title_ascending(self):

        url = reverse('barkyapi:bookmark-list') + '?ordering=title'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['title'])
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)

    def test_ordering_by_title_descending(self):
        url = reverse('barkyapi:bookmark-list') + '?ordering=-title'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['title'], reverse=True)
        # print(response_result)
        # print(expected_result)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)
    
    # 26. list bookmarks by url
    def test_ordering_by_url_ascending(self):

        url = reverse('barkyapi:bookmark-list') + '?ordering=url'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['url'])
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)

    def test_ordering_by_url_descending(self):
        url = reverse('barkyapi:bookmark-list') + '?ordering=-url'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['url'], reverse=True)
        # print(response_result)
        # print(expected_result)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)


class SnippetTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_superuser(
            username="tester", 
            email="tester@mail.com", 
            password="Pass12345")
        
        self.user2 = User.objects.create_superuser(
            username="tester2", 
            email="tester@mail.com", 
            password="Pass12345")
        
        self.client = APIClient() #add
        self.client.force_authenticate(user=self.user)
        # print(self.user)
        
        self.snippet = Snippet.objects.create(
            id=1,
            title="Awesome Django",
            code= "print(\"testing\")",
            linenos=False,
            style="friendly",
            owner=self.user
        ) 
        
        self.snippet2 = Snippet.objects.create(
            id=2,
            title="Django",
            code= "print(\"testing\")",
            linenos=False,
            style="friendly",
            owner=self.user2
        ) 
        
        # the simple router provides the name 'snippet-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:snippet-list")
        self.detail_url = reverse(
            "barkyapi:snippet-detail", kwargs={"pk": self.snippet.id}
        )
    # 6. create a snippet
    def test_create_snippet(self):
        """
        Ensure we can create a new snippet object.
        """

        # the full record is required for the POST
        data = {
            "title": "tester_snippet",
            "code": "print(\"tester\")",
            "linenos": "False",
            "language": "python",
            "style": "friendly",
            "owner": 1
        }
        response = self.client.post(self.list_url, data, format="json")
        # print("Test Create Snippet")
        # print(response.status_code)
        # print(response.data)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Snippet.objects.count(), 3)
        self.assertEqual(Snippet.objects.get(id=3).title, "tester_snippet")

    # 7. retrieve a snippet
    def test_retrieve_snippet(self):
        """
        Ensure we can retrieve a snippet object.
        """
        response = self.client.get(self.detail_url)
        # print(response.data)
        # print(response.status_code)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], self.snippet.title)

    # 8. delete a snippet
    def test_delete_snippet(self):
        """
        Ensure we can delete a snippet object.
        """
        response = self.client.delete(
            reverse("barkyapi:snippet-detail", kwargs={"pk": self.snippet.id})
        )
        # print("Test Delete Snippet")
        # print(response.data)
        # print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bookmark.objects.count(), 0)

    # 9. list snippets
    def test_list_snippets(self):
        """
        Ensure we can list all snippet objects.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"][0]["title"], self.snippet.title)

    # 10. update a snippet
    def test_update_snippet(self):
        """
        Ensure we can update a snippet object.
        """
        # the full record is required for the POST
        data = {
            "title": "Awesomer Django",
            "code": "print(\"testing_updated\")",
            "linenos": "False",
            "language": "python",
            "style": "friendly",
            "owner": 1
        }
            
        response = self.client.put(
            reverse("barkyapi:snippet-detail", kwargs={"pk": self.snippet.id}),
            data,
            format="json",
        )
        # print("Test Update Snippet")
        # print(response.data)
        # print(response.status_code)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], "Awesomer Django")  

    # 18. list snippets by user
    def test_ordering_by_userid_ascending(self):

        url = reverse('barkyapi:snippet-list') + '?ordering=id'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['id'])
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)

    def test_ordering_by_userid_descending(self):
        url = reverse('barkyapi:snippet-list') + '?ordering=-id'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['id'], reverse=True)
        # print(response_result)
        # print(expected_result)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)

    # 24. list snippets by title
    def test_ordering_by_title_ascending(self):

        url = reverse('barkyapi:snippet-list') + '?ordering=title'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['title'])
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)

    def test_ordering_by_title_descending(self):
        url = reverse('barkyapi:snippet-list') + '?ordering=-title'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['title'], reverse=True)
        # print(response_result)
        # print(expected_result)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)



class UserTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(
            username= "tester", 
            email="tester@mail.com",
            password="Pass12345"
            )
        
        self.client = APIClient() #add
    
        # the simple router provides the name 'user-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:user-list")
        self.detail_url = reverse(
            "barkyapi:user-detail", kwargs={"pk": self.user.id}
        )

    # 11. create a user
    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """

        # the full record is required for the POST
        data = {
            "username": "tester_created",
            "email": "tester_c@mail.com",
            "password": "Pass12345"
        }

        response = self.client.post(self.list_url, data, format="json")
        # print("Test Create User")
        # print(response.status_code)
        # print(response.data)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(id=2).username, "tester_created")

    # 12. retrieve a user
    def test_retrieve_user(self):
        """
        Ensure we can retrieve a user object.
        """
        response = self.client.get(self.detail_url)
        # print(response.data)
        # print(response.status_code)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["username"], self.user.username)

    # 13. delete a user
    def test_delete_user(self):
        """
        Ensure we can delete a user object.
        """
        response = self.client.delete(
            reverse("barkyapi:user-detail", kwargs={"pk": self.user.id})
        )
        # print("Delete User")
        # print(response.data)
        # print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

    # 14. list users
    def test_list_users(self):
        """
        Ensure we can list all user objects.
        """
        response = self.client.get(self.list_url)
        # print(response.data)
        # print(response.status_code)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"][0]["id"], self.user.id)

    # 15. update a user
    def test_update_user(self):
        """
        Ensure we can update a user object.
        """
        # the full record is required for the POST
        data = {
            "username": "tester",
            "email": "tester@mail.com",
            "password": "Update12345"
        }
            
        response = self.client.put(
            reverse("barkyapi:user-detail", kwargs={"pk": self.user.id}),
            data,
            format="json",
        )
        # print("Update User")
        # print(response.data)
        # print(response.status_code)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["password"], "Update12345")


# 16. highlight a snippet
# 17. list bookmarks by user
# 21. list snippets by date
# 27. list snippets by url





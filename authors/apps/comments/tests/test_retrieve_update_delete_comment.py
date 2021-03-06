import json
from django.test import TestCase
from rest_framework.test import APIClient
from authors.apps.comments.tests.base_setup import BaseCommentTests


class TestListCreateComment(BaseCommentTests):
    def test_cannot_comment_update_a_comment_without_a_token(self):
        response = self.client.put(
            f"/api/articles/{str(self.article.slug)}/comments/",
            content_type="application/json",
            data=json.dumps({"body": "Fake article"}),
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided.",
        )

    def test_cannot_comment_update_a_comment_created_by_another_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user2.token}"
        )

        response = self.client.put(
            f"/api/articles/{str(self.article.slug)}/comments/{self.comment.id}/",
            content_type="application/json",
            data=json.dumps({"comment":{"body": "Fake article"}}),
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["message"],
            "You do not have permission to perform this action.",
        )

    def test_can_comment_update_a_comment_created_by_current_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user.token}")

        response = self.client.put(
            f"/api/articles/{str(self.article.slug)}/comments/{self.comment.id}/",
            content_type="application/json",
            data=json.dumps({"comment":{"body": "Nice article"}}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["body"], "Nice article")
        self.assertEqual(
            response.data["author"]["username"], self.user.username
        )

    def test_cannot_update_a_highlighted_text_of_a_comment(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user.token}")

        response = self.client.put(
            f"/api/articles/{str(self.article.slug)}/comments/{self.comment.id}/",
            content_type="application/json",
            data=json.dumps({"comment":{
                      "body": "Nice article",
                      "start_index": 2,
                      "end_index": 2
                      }}),
        )
        self.assertEqual(response.status_code, 400)

    def test_comment_body_is_not_changed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user.token}")

        response = self.client.put(
            f"/api/articles/{str(self.article.slug)}/comments/{self.comment.id}/",
            content_type="application/json",
            data=json.dumps({"comment":{"body": "My first comment"}}),
        )
        self.assertEqual(response.status_code, 400)


    def test_cannot_delete_a_comment_created_by_another_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user2.token}"
        )

        response = self.client.delete(
            f"/api/articles/{str(self.article.slug)}/comments/{self.comment.id}/",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_can_delete_a_comment_created_by_current_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user.token}")

        response = self.client.delete(
            f"/api/articles/{str(self.article.slug)}/comments/{self.comment.id}/",
            content_type="application/json",
            data=json.dumps({"body": "Nice article"}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["message"], "Comment deleted Successfully"
        )

    def test_get_any_comment_update_a_comment_created_by_another_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user2.token}"
        )

        response = self.client.get(
            f"/api/articles/{str(self.article.slug)}/comments/{self.comment.id}/",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["body"], self.comment.body)
        self.assertEqual(
            response.data["author"]["username"], self.user.username
        )

    def test_list_comment_edit_history(self):
        test_token = self.user.token
        test_comment_id = self.comment.id
        test_slug = self.article.slug
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {test_token}")
        self.client.put(
            f"/api/articles/{str(test_slug)}/comments/{test_comment_id}/",
            content_type="application/json",
            data=json.dumps({"comment":{"body": "Very Nice article"}}),
        )
        response = self.client.get(
            f"/api/articles/{str(test_slug)}/comments/{test_comment_id}/history",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_list_comment_edit_history_no_article(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user2.token}"
        )
        response = self.client.get(
            f"/api/articles/{str(self.article.slug)}-wrong/comments/{self.comment.id}/history",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)

    def test_list_comment_edit_history_no_comment(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user2.token}"
        )
        response = self.client.get(
            f"/api/articles/{str(self.article.slug)}/comments/{self.comment.id}34/history",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)


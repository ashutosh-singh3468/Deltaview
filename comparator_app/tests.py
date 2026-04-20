from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from .forms import DocumentCompareForm
from .utils import build_diff, similarity_percent, text_stats


class DocumentCompareFormTests(TestCase):
    def test_rejects_unsupported_extension(self):
        form = DocumentCompareForm(
            files={
                'left_file': SimpleUploadedFile('left.exe', b'data'),
                'right_file': SimpleUploadedFile('right.txt', b'data'),
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('left_file', form.errors)


class UtilityFunctionTests(TestCase):
    def test_text_stats_counts_words_sentences_and_characters(self):
        stats = text_stats('Hello world. Another line!')

        self.assertEqual(stats['word_count'], 4)
        self.assertEqual(stats['sentence_count'], 2)
        self.assertEqual(stats['character_count'], 26)

    def test_similarity_percent_identical_text_is_100(self):
        self.assertEqual(similarity_percent('same content', 'same content'), 100.0)

    def test_build_diff_marks_added_content(self):
        diff = build_diff('hello world', 'hello brave world')

        self.assertNotIn('added', diff['left_html'])
        self.assertIn('added', diff['right_html'])


class CompareDocumentsViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_renders_results_even_when_similarity_is_zero(self):
        left_file = SimpleUploadedFile('left.txt', b'alpha beta gamma')
        right_file = SimpleUploadedFile('right.txt', b'one two three')

        response = self.client.post(
            reverse('compare_documents'),
            {'left_file': left_file, 'right_file': right_file},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Similarity score')
        self.assertIn('comparison_done', response.context)
        self.assertTrue(response.context['comparison_done'])

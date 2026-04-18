from django.shortcuts import render

from .forms import DocumentCompareForm
from .models import ComparisonResult
from .utils import build_diff, extract_text, similarity_percent, text_stats


def compare_documents(request):
    context = {'form': DocumentCompareForm()}

    if request.method == 'POST':
        form = DocumentCompareForm(request.POST, request.FILES)
        context['form'] = form

        if form.is_valid():
            left_file = form.cleaned_data['left_file']
            right_file = form.cleaned_data['right_file']

            left_text = extract_text(left_file)
            right_text = extract_text(right_file)

            left_stats = text_stats(left_text)
            right_stats = text_stats(right_text)
            similarity = similarity_percent(left_text, right_text)
            diff = build_diff(left_text, right_text)

            summary = (
                f"Left words: {left_stats['word_count']}, Right words: {right_stats['word_count']}, "
                f"Similarity: {similarity}%"
            )
            ComparisonResult.objects.create(
                left_file_name=left_file.name,
                right_file_name=right_file.name,
                similarity_percent=similarity,
                summary=summary,
            )

            context.update(
                {
                    'left_file_name': left_file.name,
                    'right_file_name': right_file.name,
                    'left_stats': left_stats,
                    'right_stats': right_stats,
                    'similarity': similarity,
                    'left_html': diff['left_html'],
                    'right_html': diff['right_html'],
                }
            )

    return render(request, 'comparator_app/compare.html', context)

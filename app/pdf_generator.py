"""
PDF generation utility for courses with markdown support
"""
from io import BytesIO
from weasyprint import HTML, CSS
from datetime import datetime
import markdown
import html
import re
import os


def generate_course_pdf(course_data, theme='light'):
    """
    Generate a PDF from course data

    Args:
        course_data: Dictionary containing course information
        theme: 'light' or 'dark' theme for the PDF

    Returns:
        BytesIO object containing the PDF
    """
    try:
        html_content = create_course_html(course_data)

        # Generate PDF from HTML with theme
        pdf_file = BytesIO()
        HTML(string=html_content).write_pdf(
            pdf_file,
            stylesheets=[CSS(string=get_pdf_styles(theme))]
        )
        pdf_file.seek(0)

        return pdf_file
    except Exception as e:
        # Log the error with details for debugging
        import traceback
        print(f"PDF Generation Error: {str(e)}")
        print(traceback.format_exc())
        raise Exception(f"PDF generation failed: {str(e)}")


def markdown_to_html(text):
    """
    Convert markdown text to HTML with code block support

    Args:
        text: Markdown formatted text (must be a string)

    Returns:
        HTML string
    """
    if not text:
        return ''

    # Ensure text is a string
    if isinstance(text, list):
        # If it's a list, join items with newlines
        text = '\n'.join(str(item) for item in text)
    elif not isinstance(text, str):
        # Convert to string if it's not already
        text = str(text)

    # Configure markdown with extensions
    md = markdown.Markdown(extensions=[
        'fenced_code',
        'codehilite',
        'tables',
        'nl2br',
        'sane_lists'
    ])

    # Convert markdown to HTML
    html_output = md.convert(text)

    return html_output


def escape_html(text):
    """
    Escape HTML special characters for safety

    Args:
        text: Text to escape

    Returns:
        Escaped text
    """
    if not text:
        return ''
    return html.escape(str(text))


def create_course_html(course):
    """
    Create HTML content for the course PDF

    Args:
        course: Dictionary containing course data

    Returns:
        String containing HTML content
    """
    # Extract course data with escaping for non-markdown fields
    course_id = course.get('id', '')
    name = escape_html(course.get('name', 'Untitled Course'))
    description = course.get('description', '')
    level = escape_html(course.get('level', ''))
    topic = escape_html(course.get('topic', ''))
    summary = course.get('summary', {})
    content = course.get('content', [])

    # Construct course URL
    # Get frontend URL from environment variable, default to localhost
    frontend_url = os.getenv('ALLOWED_ORIGINS', 'http://localhost:5173').split(',')[0]
    course_url = f"{frontend_url}/courses/{topic}/{course_id}" if course_id and topic else ''

    # Create summary sections
    summary_html = ''
    if summary:
        # Goal - render as markdown
        goal = summary.get('goal', '')
        if goal:
            goal_html = markdown_to_html(goal)
            summary_html += f'''
            <div class="section">
                <h2>Course Goal</h2>
                <div class="content">{goal_html}</div>
            </div>
            '''

        # Syllabus
        syllabus = summary.get('syllabus', [])
        if syllabus and isinstance(syllabus, list):
            summary_html += '''
            <div class="section">
                <h2>Syllabus</h2>
                <ul class="syllabus-list">
            '''
            for item in syllabus:
                # Each syllabus item might contain markdown
                # Ensure item is not None or empty
                if item:
                    item_html = markdown_to_html(item)
                    summary_html += f'<li>{item_html}</li>'
            summary_html += '</ul></div>'

        # Requirements (these are course IDs, just display as numbers)
        requirements = summary.get('requirements', [])
        if requirements:
            summary_html += '''
            <div class="section">
                <h2>Requirements</h2>
                <ul class="requirements-list">
            '''
            for req in requirements:
                req_escaped = escape_html(req)
                summary_html += f'<li>Course ID: {req_escaped}</li>'
            summary_html += '</ul></div>'

    # Create course content with markdown support
    lessons_html = ''
    if content:
        for idx, lesson in enumerate(content, 1):
            title = escape_html(lesson.get('title', f'Lesson {idx}'))
            body = lesson.get('body', '')
            instructions = lesson.get('instructions', '')
            expected_output = lesson.get('expected_output', '')
            conclusion = lesson.get('conclusion', '')

            lessons_html += f'<div class="lesson"><h3 class="lesson-title">Lesson {idx}: {title}</h3>'

            if body:
                body_html = markdown_to_html(body)
                lessons_html += f'<div class="lesson-content"><h4>Content</h4><div class="content">{body_html}</div></div>'

            if instructions:
                instructions_html = markdown_to_html(instructions)
                lessons_html += f'<div class="lesson-content"><h4>Instructions</h4><div class="content">{instructions_html}</div></div>'

            if expected_output:
                output_html = markdown_to_html(expected_output)
                lessons_html += f'<div class="lesson-content"><h4>Expected Output</h4><div class="content">{output_html}</div></div>'

            if conclusion:
                conclusion_html = markdown_to_html(conclusion)
                lessons_html += f'<div class="lesson-content"><h4>Conclusion</h4><div class="content">{conclusion_html}</div></div>'

            lessons_html += '</div>'

    # Convert description to markdown
    description_html = markdown_to_html(description) if description else ''

    # Build complete HTML
    html_output = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{name}</title>
    </head>
    <body>
        <div class="header">
            <h1>{name}</h1>
            {f'<p class="meta">{topic.capitalize()} | {level.capitalize()}</p>' if topic or level else ''}
            {f'<p class="course-link"><a href="{course_url}">{course_url}</a></p>' if course_url else ''}
        </div>

        {f'<div class="description"><div class="content">{description_html}</div></div>' if description else ''}

        {summary_html}

        {lessons_html}

        <div class="footer">
            <p>This course material is proprietary and confidential.</p>
        </div>
    </body>
    </html>
    '''

    return html_output


def get_pdf_styles(theme='light'):
    """
    Get CSS styles for the PDF with code formatting support

    Args:
        theme: 'light' or 'dark' theme

    Returns:
        String containing CSS styles
    """
    # Define color schemes
    if theme == 'dark':
        colors = {
            'bg': '#1e1e1e',
            'text': '#e0e0e0',
            'text_muted': '#a0a0a0',
            'heading': '#4da6ff',
            'border': '#404040',
            'lesson_bg': '#252525',
            'lesson_border': '#383838',
            'code_bg': '#2d2d2d',
            'code_border': '#404040',
            'code_text': '#e0e0e0',
            'inline_code_bg': '#2d2d2d',
            'inline_code_text': '#ff79c6',
            'blockquote_border': '#4da6ff',
            'table_header_bg': '#2d2d2d',
            'table_border': '#404040',
            'link': '#4da6ff',
            'description_bg': '#252525',
            'description_border': '#4da6ff',
        }
    else:  # light theme
        colors = {
            'bg': '#ffffff',
            'text': '#333',
            'text_muted': '#666',
            'heading': '#0066cc',
            'border': '#e9ecef',
            'lesson_bg': '#ffffff',
            'lesson_border': '#dee2e6',
            'code_bg': '#f5f5f5',
            'code_border': '#ddd',
            'code_text': '#333',
            'inline_code_bg': '#f5f5f5',
            'inline_code_text': '#d63384',
            'blockquote_border': '#0066cc',
            'table_header_bg': '#f8f9fa',
            'table_border': '#dee2e6',
            'link': '#0066cc',
            'description_bg': '#f8f9fa',
            'description_border': '#0066cc',
        }

    return f'''
        @page {{
            size: A4;
            margin: 2cm;
            background-color: {colors['bg']};
        }}

        body {{
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: {colors['text']};
            background-color: {colors['bg']};
        }}

        .header {{
            border-bottom: 3px solid {colors['heading']};
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}

        h1 {{
            font-size: 28pt;
            color: {colors['heading']};
            margin: 0 0 10px 0;
        }}

        .meta {{
            font-size: 10pt;
            color: {colors['text_muted']};
            margin: 5px 0;
        }}

        .course-link {{
            font-size: 9pt;
            color: {colors['text_muted']};
            margin-top: 10px;
        }}

        .course-link a {{
            color: {colors['link']};
            text-decoration: none;
        }}

        .description {{
            background-color: {colors['description_bg']};
            padding: 15px;
            border-left: 4px solid {colors['description_border']};
            margin-bottom: 25px;
        }}

        .section {{
            margin-bottom: 25px;
        }}

        h2 {{
            font-size: 18pt;
            color: {colors['heading']};
            border-bottom: 2px solid {colors['border']};
            padding-bottom: 8px;
            margin-top: 25px;
            margin-bottom: 15px;
        }}

        h3 {{
            font-size: 14pt;
            color: {colors['text']};
            margin-top: 20px;
            margin-bottom: 10px;
        }}

        h4 {{
            font-size: 12pt;
            color: {colors['text']};
            margin-top: 15px;
            margin-bottom: 8px;
        }}

        h5 {{
            font-size: 11pt;
            color: {colors['text_muted']};
            margin-top: 12px;
            margin-bottom: 6px;
        }}

        h6 {{
            font-size: 10pt;
            color: {colors['text_muted']};
            margin-top: 10px;
            margin-bottom: 5px;
        }}

        .lesson {{
            background-color: {colors['lesson_bg']};
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid {colors['lesson_border']};
            border-radius: 8px;
            page-break-before: always;
        }}

        .lesson-title {{
            color: {colors['heading']};
            font-size: 16pt;
            margin-top: 0;
            padding-bottom: 10px;
            border-bottom: 1px solid {colors['border']};
        }}

        .lesson-content {{
            margin-top: 15px;
        }}

        .content p:first-child {{
            margin-top: 0;
        }}

        .content p:last-child {{
            margin-bottom: 0;
        }}

        /* Code block styling */
        pre {{
            background-color: {colors['code_bg']};
            border: 1px solid {colors['code_border']};
            border-left: 4px solid {colors['heading']};
            padding: 12px;
            margin: 15px 0;
            overflow-x: auto;
            border-radius: 4px;
            font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
            font-size: 9pt;
            line-height: 1.4;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}

        code {{
            font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
            font-size: 9pt;
            background-color: {colors['inline_code_bg']};
            padding: 2px 6px;
            border-radius: 3px;
            color: {colors['inline_code_text']};
        }}

        pre code {{
            background-color: transparent;
            padding: 0;
            color: {colors['code_text']};
            border-radius: 0;
        }}

        /* Lists */
        ul, ol {{
            margin: 10px 0;
            padding-left: 25px;
        }}

        li {{
            margin-bottom: 8px;
        }}

        .syllabus-list li,
        .requirements-list li {{
            margin-bottom: 6px;
        }}

        /* Paragraphs */
        p {{
            margin: 10px 0;
            text-align: justify;
        }}

        /* Blockquotes */
        blockquote {{
            border-left: 4px solid {colors['blockquote_border']};
            padding-left: 15px;
            margin: 15px 0;
            color: {colors['text_muted']};
            font-style: italic;
        }}

        /* Tables */
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }}

        table th {{
            background-color: {colors['table_header_bg']};
            border: 1px solid {colors['table_border']};
            padding: 8px;
            text-align: left;
            font-weight: bold;
            color: {colors['text']};
        }}

        table td {{
            border: 1px solid {colors['table_border']};
            padding: 8px;
            color: {colors['text']};
        }}

        /* Horizontal rules */
        hr {{
            border: none;
            border-top: 2px solid {colors['border']};
            margin: 20px 0;
        }}

        /* Links */
        a {{
            color: {colors['link']};
            text-decoration: underline;
        }}

        /* Strong and emphasis */
        strong {{
            font-weight: bold;
        }}

        em {{
            font-style: italic;
        }}

        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid {colors['border']};
            text-align: center;
            font-size: 9pt;
            color: {colors['text_muted']};
        }}
    '''

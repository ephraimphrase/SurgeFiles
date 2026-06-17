from django import template

register = template.Library()


@register.filter
def filesize(value):
    """Convert bytes to human-readable file size."""
    try:
        value = int(value)
    except (TypeError, ValueError):
        return '0 B'

    if value < 1024:
        return f'{value} B'

    units = ['KB', 'MB', 'GB', 'TB']
    size = float(value)
    for unit in units:
        size /= 1024
        if size < 1024 or unit == 'TB':
            if size < 10:
                return f'{size:.2f} {unit}'
            elif size < 100:
                return f'{size:.1f} {unit}'
            else:
                return f'{size:.0f} {unit}'
    return f'{size:.0f} PB'


@register.filter
def file_icon(filename):
    """Return a Bootstrap Icon class based on the file extension."""
    if not filename:
        return 'bi-file-earmark'

    name = str(filename)
    ext = name.rsplit('.', 1)[-1].lower() if '.' in name else ''

    icon_map = {
        # Documents
        'pdf': 'bi-file-earmark-pdf-fill',
        'doc': 'bi-file-earmark-word-fill',
        'docx': 'bi-file-earmark-word-fill',
        'odt': 'bi-file-earmark-word-fill',
        'xls': 'bi-file-earmark-excel-fill',
        'xlsx': 'bi-file-earmark-excel-fill',
        'csv': 'bi-file-earmark-spreadsheet',
        'ppt': 'bi-file-earmark-ppt-fill',
        'pptx': 'bi-file-earmark-ppt-fill',
        'txt': 'bi-file-earmark-text-fill',
        'rtf': 'bi-file-earmark-text-fill',
        # Images
        'jpg': 'bi-file-earmark-image-fill',
        'jpeg': 'bi-file-earmark-image-fill',
        'png': 'bi-file-earmark-image-fill',
        'gif': 'bi-file-earmark-image-fill',
        'svg': 'bi-file-earmark-image-fill',
        'webp': 'bi-file-earmark-image-fill',
        'bmp': 'bi-file-earmark-image-fill',
        'ico': 'bi-file-earmark-image-fill',
        # Video
        'mp4': 'bi-file-earmark-play-fill',
        'avi': 'bi-file-earmark-play-fill',
        'mov': 'bi-file-earmark-play-fill',
        'mkv': 'bi-file-earmark-play-fill',
        'wmv': 'bi-file-earmark-play-fill',
        'webm': 'bi-file-earmark-play-fill',
        # Audio
        'mp3': 'bi-file-earmark-music-fill',
        'wav': 'bi-file-earmark-music-fill',
        'flac': 'bi-file-earmark-music-fill',
        'aac': 'bi-file-earmark-music-fill',
        'ogg': 'bi-file-earmark-music-fill',
        # Archives
        'zip': 'bi-file-earmark-zip-fill',
        'rar': 'bi-file-earmark-zip-fill',
        '7z': 'bi-file-earmark-zip-fill',
        'tar': 'bi-file-earmark-zip-fill',
        'gz': 'bi-file-earmark-zip-fill',
        'bz2': 'bi-file-earmark-zip-fill',
        # Code
        'py': 'bi-file-earmark-code-fill',
        'js': 'bi-file-earmark-code-fill',
        'ts': 'bi-file-earmark-code-fill',
        'html': 'bi-file-earmark-code-fill',
        'css': 'bi-file-earmark-code-fill',
        'java': 'bi-file-earmark-code-fill',
        'cpp': 'bi-file-earmark-code-fill',
        'c': 'bi-file-earmark-code-fill',
        'rb': 'bi-file-earmark-code-fill',
        'go': 'bi-file-earmark-code-fill',
        'rs': 'bi-file-earmark-code-fill',
        'json': 'bi-file-earmark-code-fill',
        'xml': 'bi-file-earmark-code-fill',
        'yaml': 'bi-file-earmark-code-fill',
        'yml': 'bi-file-earmark-code-fill',
    }
    return icon_map.get(ext, 'bi-file-earmark-fill')


@register.filter
def file_icon_color(filename):
    """Return a CSS color class based on file type category."""
    if not filename:
        return 'text-secondary'

    name = str(filename)
    ext = name.rsplit('.', 1)[-1].lower() if '.' in name else ''

    color_map = {
        'pdf': 'text-danger',
        'doc': 'text-primary', 'docx': 'text-primary', 'odt': 'text-primary',
        'xls': 'text-success', 'xlsx': 'text-success', 'csv': 'text-success',
        'ppt': 'text-warning', 'pptx': 'text-warning',
        'jpg': 'text-info', 'jpeg': 'text-info', 'png': 'text-info',
        'gif': 'text-info', 'svg': 'text-info', 'webp': 'text-info',
        'bmp': 'text-info', 'ico': 'text-info',
        'mp4': 'text-purple', 'avi': 'text-purple', 'mov': 'text-purple',
        'mkv': 'text-purple', 'wmv': 'text-purple', 'webm': 'text-purple',
        'mp3': 'text-pink', 'wav': 'text-pink', 'flac': 'text-pink',
        'aac': 'text-pink', 'ogg': 'text-pink',
        'zip': 'text-warning', 'rar': 'text-warning', '7z': 'text-warning',
        'tar': 'text-warning', 'gz': 'text-warning',
        'py': 'text-success', 'js': 'text-warning', 'ts': 'text-primary',
        'html': 'text-danger', 'css': 'text-primary', 'java': 'text-danger',
    }
    return color_map.get(ext, 'text-secondary')

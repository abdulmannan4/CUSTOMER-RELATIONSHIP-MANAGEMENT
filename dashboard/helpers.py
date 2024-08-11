from io import BytesIO
import uuid
import os
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa

def pdf_generator(context: dict):
    '''
    Function to generate PDF file and save it to the media directory.
    '''
    template = get_template('pdf_generator/data.html')
    html = template.render(context=context)

    # Generate unique file name
    file_name = uuid.uuid4()

    # Prepare file path
    file_path = os.path.join(settings.MEDIA_ROOT,'media', f'{file_name}.pdf')

    try:
        # Generate PDF and write to file
        with open(file_path, 'wb+') as output:
            pisa_status = pisa.pisaDocument(BytesIO(html.encode('utf-8')), output)
            
            # Check if PDF generation was successful
            if pisa_status.err:
                return '', False
    except Exception as e:
        print(f"Failed to generate PDF: {e}")
        return '', False

    return file_name, True

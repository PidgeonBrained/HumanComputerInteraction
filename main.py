class TextRectException:
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message


def render_textrect(string, font, rect, text_color, background_color, justification=0):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """

    import pygame

    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise  "The word " + word + " is too long to fit in the rect passed."
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line
                else:
                    final_lines.append(accumulated_line)
                    accumulated_line = word + " "
            final_lines.append(accumulated_line)
        else:
            final_lines.append(requested_line)

            # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size)
    surface.fill(background_color)

    accumulated_height = 0
    for line in final_lines:
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise  "Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise  "Invalid justification argument: " + str(justification)
        accumulated_height += font.size(line)[1]

    return surface


if __name__ == '__main__':
    import pygame
    import pygame.font
    from pygame.locals import *

    pygame.init()

    display = pygame.display.set_mode((1000, 1000))

    my_font = pygame.font.Font(None, 22)
    my_string="INFORMED CONSENT DOCUMENT \n Please read the following informed consent document. \n If you consent to the study, please press the continue button. If you do not consent and would like to cancel your participation in the study, press escape. \n Project Title:	 CS470 HCI – Fitts’ Law study\n Research Team:\nPidge Witiak - (chase.witiak@mnsu .edu)\nSam Baeyen - (samuel.baeyen@mnsu.edu)\nAhmed Alqadoucy - (ahmed.alqadoucy@mnsu.edu)\nCole Schoenbauer - (cole.schoenbauer@mnsu.edu)\nThank you for agreeing to participate in this research study! This document provides important information about what you will be asked to do during the research study, about the risks and benefits of the study, and about your rights as a research subject. If you have any questions about or do not understand something in this document, you should ask questions to the members of the research team listed above. Do not agree to participate in this research study unless the research team has answered your questions and you decide that you want to be part of this study."
# The purpose of this research study is to evaluate how accurately a user can click on differently-sized sqaures on screen. During the study, you will be randomly presented with ____ squares to click. There will be a total of ___ trials, and each trial will take anywhere from ___ to ___ seconds, depending on your speed. The entire study should take no longer than ___ minutes to complete.
# To participate in this study, you must …
# To collect data, our software will record how much you move the mouse, how long it takes you to successfully complete each trial, and whether you make any errors. This information will be recorded anonymously, and no personally identifiable information will be collected.
# You will not be compensated for your participation in this study. We do not believe there are any direct benefits to you based on your participation in the study. We do not anticipate any significant risks in your participating in this study.
# You may end your participation in the study at any time. If you wish to end your participation, please notify one of the researchers. If you decide to end your participation early, any results collected by the software for your session will not be saved.
# By digitally signing this document, you hereby acknowledge that you are at least 18 years of age, and that you are (other inclusion criteria). You also indicate that you agree to the following statement:
# “I have read this consent form and I understand the risks, benefits, and procedures involved with participation in this research study. I hereby agree to participate in this research study.”
# "
    my_rect = pygame.Rect((40, 40, 1300, 1300))

    rendered_text = render_textrect(my_string, my_font, my_rect, (216, 216, 216), (48, 48, 48), 0)

    if rendered_text:
        display.blit(rendered_text, my_rect.topleft)

    pygame.display.update()

    while not pygame.event.wait().type in (QUIT, KEYDOWN):
        pass
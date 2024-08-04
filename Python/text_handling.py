import global_constants as gc

class TextBundle:
	def __init__(
			self, 
			text, 
			font=gc.BASIC_FONT, 
			color=gc.TEXT_COLOR, 
			font_size=gc.FONT_SIZE
		):
		self.text      = text
		self.font      = font
		self.color     = color
		self.font_size = font_size

def make_text(DISPLAY_SURF, bgcolor, top, left, text_width, *text_bundles):
	# NOTE: The newline character "\n" does work, but it _must_ be
	# separated with spaces on both sides, or at the end of your text
	# string.
	line = 0
	ending_position = left
	for text_bundle in text_bundles:
		words = text_bundle.text.split(" ")
		current_line = ""
		for word in words:
			textSurf = text_bundle.font.render(
				current_line, True, text_bundle.color, bgcolor
			)
			nextSurf = text_bundle.font.render(
				current_line + word + " ", True, text_bundle.color, bgcolor
			)
			if (
				nextSurf.get_width() + (ending_position - left) <= text_width
			) and word != "\n":
				current_line += word + " "
			else:
				textRect = textSurf.get_rect()
				textRect.topleft = (
					ending_position, top + line * text_bundle.font_size
				)
				ending_position = left
				DISPLAY_SURF.blit(textSurf, textRect)
				if word != "\n":
					current_line = "" + word + " "
				else:
					current_line = ""
				line += 1
		# Print the final line.
		if current_line != " ": # Don't print lone spaces after \n.
			textSurf = text_bundle.font.render(
				current_line, True, text_bundle.color, bgcolor
			)
			textRect = textSurf.get_rect()
			textRect.topleft = (
				ending_position, top + line * text_bundle.font_size
			)
			ending_position = textRect.right
			DISPLAY_SURF.blit(textSurf, textRect)
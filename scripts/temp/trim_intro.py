
# Trims pages/introduction.html to Chapter 1 only.
# Keeps: lines 1-242 (head + nav + §1 Introduction + divider)
# Replaces: lines 243-1199 with a minimal close block

with open(r'c:/Users/elgin/Documents/GitHub/IS431/pages/introduction.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Keep everything up to and including the sl-divider after Ch.1 (line 242)
head = lines[:242]

# Build minimal close: closing .content div, scroll-to-top button, close body/html
tail = [
    '\n',
    '  </div><!-- /.content -->\n',
    '\n',
    '  <!-- Scroll to top -->\n',
    '  <sl-button class="scroll-to-top" variant="primary" size="medium" circle onclick="scrollToTop()">\n',
    '    <sl-icon name="arrow-up" label="Back to top"></sl-icon>\n',
    '  </sl-button>\n',
    '\n',
    '</body>\n',
    '</html>\n',
]

result = head + tail

with open(r'c:/Users/elgin/Documents/GitHub/IS431/pages/introduction.html', 'w', encoding='utf-8') as f:
    f.writelines(result)

print('Done. File now has', len(result), 'lines.')

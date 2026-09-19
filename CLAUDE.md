# Two-Hour Technical Webinar

This CLAUDE.md file serves as a guide for preparing the instructor materials for the webinar regardless of topic. This file is copied from webinar to webinar. Anything specific to a particular webinar belongs in the repo `README.md`, not in this file.

## Overview

This is a repo for a 2-hour webinar. The webinar runs for 1.5 hours during the 2-hour session. You will create the number of demos appropriate for the session. The slide deck should cover all of the key points in the agenda and support the demos effectively. The slides should take no more than 20 minutes with the remaining time allocated for demos. The presenter will answer questions while waiting for the demos to run.

The repo `README.md` contains the title, description and agenda for the webinar. The repo will contain a slide deck in the `docs` folder, demos in the `demos` folder, and instructor materials in the `instructor` folder. Before delivery of the webinar, the presenter will delete the `instructor` folder.

The presenter name is "Eric Greene", the company is "Xebia". The presenters email address is "eric.greene@xebia.com". There is no delivery date.

The audience will be technical professionals interested in the topic described in the repo `README.md`. Assume they are comfortable with a terminal and with reading code, but do not assume they have used the specific tools the webinar covers.

If you need a fact about this particular webinar that isn't in the `README.md` file, such as the presenter name, ask the presenter rather than inventing one.

## Folders

### docs Folder

I am looking for around 15 slides 8 of which will be content slides. The remaining 7 slides will be title slides, demo slide, questions slide, next steps, etc. Use the `Xebia PPT General Template.pptx` file in the `instructor` folder as the template for the slide deck. Create a new PPT file using the PDF file name (minus the ext) found in the repo `README.md` file.

The content slides should cover the agenda in the `README.md` file. When there are fewer agenda items than content slides, give the extra slides to the topics that carry the most weight for the demos. Include speaker notes on every slide. The notes are a summary for the presenter's own reference; the word-for-word script lives in the `instructor` folder.

You need to produce a new PDF file from the slide deck after making any edits to the PPT file. Use LibreOffice, which is installed locally but is not on the PATH, to convert from PPT to PDF:

```
& "C:\Program Files\LibreOffice\program\soffice.exe" --headless --convert-to pdf --outdir docs docs\<slide-deck-name>.pptx
```

The conversion fails quietly if the PPT file is open in PowerPoint, so close it first.

### demos Folder

The demos should show the tools and the workflow the webinar teaches, not just the finished code. Any application code produced along the way will be written in Python, and the `uv` tool will be used to configure virtual environments for each demo and run them.

Each demo lives in its own folder under `demos` with its own `pyproject.toml` managed by `uv` and a pinned Python version. A demo has to run offline on the presenter's machine without paid services or API keys, apart from the AI coding tools the webinar is about. No single demo should take more than 20 minutes to walk through.

Each demo will have a `README.md` file containing the instructions for the demo and presentation trail. The presentation trail is for the presenter and student to follow during the webinar. Each step in the trail should mention the file being reviewed and explain the code. The demo instructions are for the presenter and students, and they should open with any tools the student needs installed before starting. The `demos` folder should have a `README.md` file that provides a list of all of the demos, a short name and description, and a link to the demo `README.md` file.

Webinar specific demo instructions are located in the `CLAUDE.md` file in the `demos` folder.

### instructor Folder

Use the `CLAUDE.md` file in the `instructor` folder as a guide for preparing the instructor materials.

## Content Style

- Humanize the language in all of the content including the slides, code comments, and other documents.
- The content should sound like a professional, corporate technical trainer wrote the content.
- Avoid jargon and overly complex language; aim for clarity and simplicity.
- Do not use short declarative zingers. The language should be professional.
- Contractions are allowed and encouraged.
- Unbalanced sentences are acceptable if they contribute to a more natural, human-like flow of the content.
- Ensure all content is appropriate for a professional and corporate audience.
- Maintain a consistent tone and style throughout all materials, including slides, code comments, and documentation.
- Slides should not be dense. Keep content slides to six bullets or fewer, and keep each bullet under a dozen words. Code on a slide should fit comfortably without shrinking the font.
- Each artifact reads a little differently. Slides can use fragments. The script is meant to be read aloud, so it should sound like speech. Code comments explain why the code does what it does, not what it does.

## Definition of Done

The slide deck, the PDF, the teaching guide, the script, and the demos drift apart easily. After any change, work through this list:

- The PDF in the `docs` folder was regenerated from the current PPT file.
- The slide count and the agenda in the `README.md` file still match the deck.
- Every slide has speaker notes, and the script in the `instructor` folder matches the current slides.
- Every demo runs clean with `uv` from a fresh clone.
- Every relative link in the `README.md` files resolves.
- Nothing in the `docs` or `demos` folders depends on the `instructor` folder, since the presenter deletes it before delivery.

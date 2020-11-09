from pathlib import Path

import frontmatter
import typer


def main(
    show_categories: bool = typer.Option(False, '--categories/--no-categories', help='show categories'),
    show_tags: bool = typer.Option(False, '--tags/--no-tags', help='show tags')
):
    if not (show_categories or show_tags):
        raise typer.Exit('Did not choose to print categories or tags')

    categories = set()
    tags = set()

    for file in Path('.').glob('_posts/*.md'):
        metadata, _ = frontmatter.parse(file.open().read())
        post_categories = metadata.get('categories')

        if isinstance(post_categories, list):
            categories.update(set(post_categories))
        elif isinstance(post_categories, str):
            categories.add(post_categories)

        post_tags = metadata.get('tags')
        if post_tags:
            tags.update(set(post_tags))

    if show_categories:
        print('\n'.join(categories))

    if show_tags:
        print('\n'.join(tags))


if __name__ == '__main__':
    typer.run(main)

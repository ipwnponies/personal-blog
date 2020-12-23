from collections import defaultdict, Counter
from pathlib import Path

import frontmatter
import tabulate
import typer


def main(
    show_categories: bool = typer.Option(False, '--categories/--no-categories', help='show categories'),
    show_tags: bool = typer.Option(False, '--tags/--no-tags', help='show tags')
):
    if not (show_categories or show_tags):
        raise typer.Exit('Did not choose to print categories or tags')

    categories = defaultdict(int)
    tags = defaultdict(int)

    for file in Path('.').glob('_posts/*.md'):
        metadata, _ = frontmatter.parse(file.open().read())
        post_categories = metadata.get('categories') or []

        if isinstance(post_categories, str):
            post_categories = [post_categories]

        for i in post_categories:
            categories[i] += 1

        post_tags = metadata.get('tags') or []
        for i in post_tags:
            tags[i] += 1

    if show_categories:
        print(tabulate.tabulate(
            Counter(categories).most_common(),
            headers=['category', 'count']
        ))

    if show_tags:
        print(tabulate.tabulate(
            Counter(tags).most_common(),
            headers=['tag', 'count']
        ))


if __name__ == '__main__':
    typer.run(main)

import click
from typing import List, Tuple

from fds_dev.rules import LintError

class OutputFormatter:
    def display_lint_results(self, results: List[Tuple[str, List[LintError]]]):
        """
        Displays a formatted list of linting errors, grouped by file.
        """
        total_errors = 0
        files_with_errors = 0
        
        for file_path, errors in results:
            if errors:
                files_with_errors += 1
                error_count = len(errors)
                total_errors += error_count
                plural = 's' if error_count > 1 else ''
                
                click.secho(f"\n❌ Found {error_count} issue{plural} in {file_path}:")
                for error in sorted(errors, key=lambda e: e.line_number):
                    line_info = f"L{error.line_number:<4}"
                    rule_info = f"({error.rule_name})"
                    click.echo(f"  - {line_info} {click.style(rule_info, fg='yellow'):<25} {error.message}")

        if total_errors == 0:
            file_count = len(results)
            plural = 's' if file_count > 1 else ''
            click.secho(f"\n✅ No issues found in {file_count} file{plural}.", fg="green")
        else:
            click.echo("-" * 40)
            click.secho(f"Summary: Found {total_errors} total issues in {files_with_errors} files.", bold=True)


    def display_translation_preview(self, original_path: str, translated_content: str):
        """
        Displays a preview of the translated content.
        """
        click.secho(f"\nTranslation Preview for {original_path}:", bold=True)
        click.echo("-" * 40)
        for i, line in enumerate(translated_content.splitlines()):
            if i >= 10:
                click.echo("...")
                break
            click.echo(line)
        click.echo("-" * 40)
        click.secho("Use --output or --in-place to save the translation.", fg="cyan")

    def display_save_message(self, output_path: str, in_place: bool):
        """
        Displays a message confirming the file was saved.
        """
        if in_place:
            message = f"✅ Successfully translated and saved {output_path} in-place."
        else:
            message = f"✅ Translation successfully saved to {output_path}."
        click.secho(message, fg="green")
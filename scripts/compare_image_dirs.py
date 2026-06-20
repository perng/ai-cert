#!/usr/bin/env python3
"""Compare two image directories by filename and file content."""

from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


DEFAULT_LEFT = Path("~/ai-cert/assets/images").expanduser()
DEFAULT_RIGHT = Path("~/ai-planner/assets/images").expanduser()


@dataclass(frozen=True)
class FileInfo:
    relpath: str
    size: int
    sha256: str


def iter_files(root: Path, follow_symlinks: bool) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if path.is_symlink() and not follow_symlinks:
            continue
        if path.is_file():
            files.append(path)
    return sorted(files)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scan(root: Path, follow_symlinks: bool) -> dict[str, FileInfo]:
    if not root.exists():
        raise FileNotFoundError(f"Directory does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    files: dict[str, FileInfo] = {}
    for path in iter_files(root, follow_symlinks):
        relpath = path.relative_to(root).as_posix()
        files[relpath] = FileInfo(
            relpath=relpath,
            size=path.stat().st_size,
            sha256=sha256_file(path),
        )
    return files


def build_hash_index(files: dict[str, FileInfo]) -> dict[str, list[str]]:
    by_hash: dict[str, list[str]] = defaultdict(list)
    for relpath, info in files.items():
        by_hash[info.sha256].append(relpath)
    return {hash_value: sorted(paths) for hash_value, paths in by_hash.items()}


def print_list(title: str, rows: list[str], limit: int | None) -> None:
    print(f"\n{title}: {len(rows)}")
    shown = rows if limit is None else rows[:limit]
    for row in shown:
        print(f"  {row}")
    if limit is not None and len(rows) > limit:
        print(f"  ... {len(rows) - limit} more")


def print_table(title: str, rows: list[tuple[str, int, int]], limit: int | None) -> None:
    print(f"\n{title}: {len(rows)}")
    shown = rows if limit is None else rows[:limit]
    if shown:
        print("  file\tleft_size\tright_size")
    for relpath, left_size, right_size in shown:
        print(f"  {relpath}\t{left_size}\t{right_size}")
    if limit is not None and len(rows) > limit:
        print(f"  ... {len(rows) - limit} more")


def print_mapping(title: str, rows: list[tuple[str, list[str]]], limit: int | None) -> None:
    print(f"\n{title}: {len(rows)}")
    shown = rows if limit is None else rows[:limit]
    for source, matches in shown:
        print(f"  {source} -> {', '.join(matches)}")
    if limit is not None and len(rows) > limit:
        print(f"  ... {len(rows) - limit} more")


def compare(
    left_root: Path,
    right_root: Path,
    limit: int | None,
    follow_symlinks: bool,
) -> int:
    left = scan(left_root, follow_symlinks)
    right = scan(right_root, follow_symlinks)

    left_names = set(left)
    right_names = set(right)
    common_names = sorted(left_names & right_names)
    only_left = sorted(left_names - right_names)
    only_right = sorted(right_names - left_names)

    same_name_same_content = [
        name for name in common_names if left[name].sha256 == right[name].sha256
    ]
    same_name_different_content = [
        (name, left[name].size, right[name].size)
        for name in common_names
        if left[name].sha256 != right[name].sha256
    ]

    left_hashes = build_hash_index(left)
    right_hashes = build_hash_index(right)

    left_only_content_elsewhere = [
        (name, right_hashes[left[name].sha256])
        for name in only_left
        if left[name].sha256 in right_hashes
    ]
    right_only_content_elsewhere = [
        (name, left_hashes[right[name].sha256])
        for name in only_right
        if right[name].sha256 in left_hashes
    ]

    left_missing_by_content = [
        name for name, info in sorted(left.items()) if info.sha256 not in right_hashes
    ]
    right_missing_by_content = [
        name for name, info in sorted(right.items()) if info.sha256 not in left_hashes
    ]

    left_only_no_content_match = [
        name for name in only_left if left[name].sha256 not in right_hashes
    ]
    right_only_no_content_match = [
        name for name in only_right if right[name].sha256 not in left_hashes
    ]

    print(f"Left:  {left_root}")
    print(f"Right: {right_root}")
    print(f"Follow symlinks: {follow_symlinks}")
    print()
    print(f"Left file count: {len(left)}")
    print(f"Right file count: {len(right)}")
    print(f"Common filenames: {len(common_names)}")
    print(f"Same filename and same content: {len(same_name_same_content)}")
    print(f"Same filename but different content: {len(same_name_different_content)}")
    print(f"Only in left by filename: {len(only_left)}")
    print(f"Only in right by filename: {len(only_right)}")
    print(f"Left files with no content match in right: {len(left_missing_by_content)}")
    print(f"Right files with no content match in left: {len(right_missing_by_content)}")

    print_table(
        "Same filename but different content",
        same_name_different_content,
        limit,
    )
    print_list("Only in left by filename", only_left, limit)
    print_list("Only in right by filename", only_right, limit)
    print_mapping(
        "Only-in-left names whose content exists in right under another name",
        left_only_content_elsewhere,
        limit,
    )
    print_mapping(
        "Only-in-right names whose content exists in left under another name",
        right_only_content_elsewhere,
        limit,
    )
    print_list(
        "Only-in-left names with no content match in right",
        left_only_no_content_match,
        limit,
    )
    print_list(
        "Only-in-right names with no content match in left",
        right_only_no_content_match,
        limit,
    )

    return 1 if same_name_different_content or only_left or only_right else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare two directories by relative filename and SHA-256 content.",
    )
    parser.add_argument(
        "left",
        nargs="?",
        type=Path,
        default=DEFAULT_LEFT,
        help=f"left directory, default: {DEFAULT_LEFT}",
    )
    parser.add_argument(
        "right",
        nargs="?",
        type=Path,
        default=DEFAULT_RIGHT,
        help=f"right directory, default: {DEFAULT_RIGHT}",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="limit rows printed in each detailed section",
    )
    parser.add_argument(
        "--follow-symlinks",
        action="store_true",
        help="include symlinked file entries and compare their target bytes",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return compare(
        args.left.expanduser(),
        args.right.expanduser(),
        args.limit,
        args.follow_symlinks,
    )


if __name__ == "__main__":
    raise SystemExit(main())

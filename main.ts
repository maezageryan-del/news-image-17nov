/**
 * Entry point for "The World in One Day — Tuesday 17 November 2026".
 *
 * The artwork is a finished front page that ships in this repository as
 * entry.png. The bounty harness expects the deliverable to appear at
 * $MAKEFUN_OUTPUT_DIR/entry.png, so this module's whole job is to carry the
 * page from here to there — carefully, and with clear errors if anything on
 * the way is missing.
 */

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const PAGE_NAME = "entry.png";

function fail(message: string): never {
  console.error(`the-world-in-one-day: ${message}`);
  process.exit(1);
}

function main(): void {
  // Where the harness wants the deliverable.
  const outDir = process.env.MAKEFUN_OUTPUT_DIR;
  if (!outDir || outDir.trim() === "") {
    fail("MAKEFUN_OUTPUT_DIR is not set; nowhere to deliver the page.");
  }

  // Where the finished page lives: beside this file.
  const here = dirname(fileURLToPath(import.meta.url));
  const source = join(here, PAGE_NAME);
  if (!existsSync(source)) {
    fail(`source page not found at ${source}`);
  }
  const sourceSize = statSync(source).size;
  if (sourceSize === 0) {
    fail(`source page at ${source} is empty.`);
  }

  // Refuse the degenerate case where the output folder is this folder:
  // copying the page onto itself would prove nothing and could corrupt it.
  const target = join(outDir, PAGE_NAME);
  if (resolve(target) === resolve(source)) {
    fail(`destination ${target} is the source page itself; refusing to copy a file onto itself.`);
  }

  // Make sure the destination folder exists, then copy.
  try {
    mkdirSync(outDir, { recursive: true });
    copyFileSync(source, target);
  } catch (err) {
    fail(`could not copy the page to ${target}: ${(err as Error).message}`);
  }

  // Confirm the copy arrived whole before calling it done.
  const targetSize = existsSync(target) ? statSync(target).size : -1;
  if (targetSize !== sourceSize) {
    fail(
      `copy looks incomplete: source is ${sourceSize} bytes, ` +
        `destination is ${targetSize} bytes.`,
    );
  }

  console.log(`the-world-in-one-day: delivered ${PAGE_NAME} (${sourceSize} bytes) to ${target}`);
}

main();

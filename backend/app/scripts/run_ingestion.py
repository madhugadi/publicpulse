"""
CLI Runner for PublicPulse Ingestion

Usage:
    python -m app.scripts.run_ingestion

This script:
- Reads titles from backend/data/input/items.json
- Runs ingestion for all movies and gadgets
- Updates cached JSON output
- Does NOT require FastAPI to be running
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.core.ingestion import run_ingestion


def main():
    """Main CLI entry point"""
    print("=" * 60)
    print("PublicPulse Phase 0 - Ingestion Runner")
    print("=" * 60)

    try:
        results = run_ingestion()

        # Print summary
        print("\n" + "=" * 60)
        print("INGESTION COMPLETE")
        print("=" * 60)

        movies_success = sum(1 for r in results["movies"] if r.get("success"))
        movies_failed = len(results["movies"]) - movies_success

        gadgets_success = sum(1 for r in results["gadgets"] if r.get("success"))
        gadgets_failed = len(results["gadgets"]) - gadgets_success

        print(f"\nMovies:  {movies_success} succeeded, {movies_failed} failed")
        print(f"Gadgets: {gadgets_success} succeeded, {gadgets_failed} failed")

        # Show failures if any
        failures = []
        for result in results["movies"]:
            if not result.get("success"):
                failures.append(f"  - Movie: {result['item_name']} ({result.get('error', 'Unknown error')})")

        for result in results["gadgets"]:
            if not result.get("success"):
                failures.append(f"  - Gadget: {result['item_name']} ({result.get('error', 'Unknown error')})")

        if failures:
            print("\nFailures:")
            for failure in failures:
                print(failure)

        print()

        # Exit with appropriate code
        sys.exit(0 if not failures else 1)

    except FileNotFoundError as e:
        print(f"\nERROR: {e}")
        print("\nPlease create backend/data/input/items.json with structure:")
        print('{\n  "movies": ["Movie Title 1", "Movie Title 2"],')
        print('  "gadgets": ["Gadget Name 1", "Gadget Name 2"]\n}')
        sys.exit(1)

    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

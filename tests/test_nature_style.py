from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib as mpl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from nature_style import figure_size, label_panels, new_figure, save_figure, significance_text


class NatureStyleTests(unittest.TestCase):
    def test_dimensions_and_p_values(self):
        width, height = figure_size("single", aspect=0.5)
        self.assertAlmostEqual(width, 89 / 25.4)
        self.assertAlmostEqual(height, 44.5 / 25.4)
        self.assertEqual(significance_text(0.02), "p = 0.02")
        self.assertEqual(significance_text(0.00001), "p < 0.0001")

    def test_vector_and_raster_exports(self):
        fig, axes = new_figure("single", ncols=2)
        label_panels(axes)
        for ax in axes:
            ax.plot([0, 1], [0, 1])
        with tempfile.TemporaryDirectory() as directory:
            paths = save_figure(fig, Path(directory) / "figure")
            self.assertEqual({path.suffix for path in paths}, {".svg", ".pdf", ".png"})
            self.assertTrue(all(path.stat().st_size > 0 for path in paths))
        plt.close(fig)

    def test_packaged_mplstyle_loads(self):
        with mpl.rc_context():
            plt.style.use(ROOT / "assets" / "nature.mplstyle")
            self.assertEqual(mpl.rcParams["svg.fonttype"], "none")


if __name__ == "__main__":
    unittest.main()

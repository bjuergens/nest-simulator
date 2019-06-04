# -*- coding: utf-8 -*-
#
# test_create_spatial.py
#
# This file is part of NEST.
#
# Copyright (C) 2004 The NEST Initiative
#
# NEST is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# NEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NEST.  If not, see <http://www.gnu.org/licenses/>.

"""
Tests Create with spacial specifications (create a layer)
"""

import unittest
import nest


class CreateLayer(unittest.TestCase):

    def setUp(self):
        nest.ResetKernel()

    def test_Create_grid(self):
        """Test Create simple grid."""
        layer = nest.Create('iaf_psc_alpha',
                            positions=nest.spatial.grid(rows=3, columns=3))

        self.assertEqual(len(layer), 9)
        self.assertEqual(layer.spatial['rows'], 3)

    def test_Create_grid_with_extent(self):
        """Test Create simple grid with extent."""
        layer = nest.Create('iaf_psc_alpha',
                            positions=nest.spatial.grid(rows=3, columns=3,
                                                        extent=[2., 2.]))

        self.assertEqual(layer.spatial['extent'], (2., 2.))

    def test_Create_grid_with_nodeParams(self):
        """Test Create grid layer with node parameters."""
        layer = nest.Create('iaf_psc_alpha',
                            positions=nest.spatial.grid(rows=3, columns=3),
                            params={'V_m': nest.random.uniform(),
                                    'C_m': 200.})

        self.assertEqual(layer.get('C_m'), (200.,)*len(layer))
        self.assertEqual(len(layer.get('V_m')), len(layer))
        self.assertGreaterEqual(min(layer.get('V_m')), 0.)

    def test_Create_free_layer(self):
        """Test Create simple free layer."""
        pos = ((1., 1.), (2., 2.), (3., 3.))
        layer = nest.Create('iaf_psc_alpha',
                            positions=nest.spatial.free(pos))

        self.assertEqual(len(layer), 3)
        self.assertEqual(layer.spatial['positions'], pos)

    def test_Create_free_layer_from_LognormalParameter(self):
        """Test Create free layer from lognormal parameter."""
        layer = nest.Create('iaf_psc_alpha', 33,
                            positions=nest.spatial.free(
                                nest.random.lognormal(mean=1.,
                                                      sigma=2.,
                                                      dimension=2)))

        self.assertEqual(len(layer), 33)
        self.assertEqual(len(layer.spatial['positions']), 33)
        self.assertGreaterEqual(min(min(layer.spatial['positions'])), 0)

    def test_Create_3D_free_layer_from_LognormalParameter(self):
        """Test Create 3D free layer from lognormal parameter."""
        layer = nest.Create('iaf_psc_alpha', 33,
                            positions=nest.spatial.free(
                                nest.random.lognormal(mean=(1., 2., 0.5),
                                                      sigma=(2., 2., 2.))))

        self.assertEqual(len(layer), 33)
        self.assertEqual(len(layer.spatial['positions']), 33)
        self.assertEqual(len(layer.spatial['positions'][0]), 3)

    def test_Create_free_layer_with_nodeParams(self):
        """Test Create free layer with nodeParams."""
        layer = nest.Create('iaf_psc_alpha', 33,
                            positions=nest.spatial.free(
                                nest.random.lognormal(mean=1.,
                                                      sigma=2.,
                                                      dimension=3)),
                            params={'V_m': nest.random.uniform(),
                                    'C_m': 200.})

        self.assertEqual(layer.get('C_m'), (200.,)*len(layer))
        self.assertEqual(len(layer.get('V_m')), 33)
        self.assertLessEqual(max(layer.get('V_m')), 1.)
        self.assertEqual(len(layer.spatial['positions'][0]), 3)

    def test_Create_free_layer_from_uniform_Parameter(self):
        """Test Create free layer from uniform parameter."""
        layer = nest.Create('iaf_psc_alpha', 6,
                            positions=nest.spatial.free(
                                nest.random.uniform(dimension=2)))

        self.assertEqual(len(layer), 6)
        self.assertEqual(len(layer.spatial['positions']), 6)
        self.assertGreaterEqual(min(min(layer.spatial['positions'])), 0)

    def test_Create_3D_free_layer_from_uniformParameter(self):
        """Test Create 3D free layer from uniform parameter."""
        layer = nest.Create('iaf_psc_alpha', 7,
                            positions=nest.spatial.free(
                                nest.random.uniform(min=(1., 2., 0.5),
                                                    max=(5., 2.5, 2.))))

        self.assertEqual(len(layer.spatial['positions']), 7)
        self.assertEqual(len(layer.spatial['positions'][0]), 3)

    def test_Create_free_layer_from_normal_Parameter(self):
        """Test Create free layer from normal parameter."""
        layer = nest.Create('iaf_psc_alpha', 6,
                            positions=nest.spatial.free(
                                nest.random.normal(loc=(0.0, 1.0),
                                                   scale=(0.5, 1.0))))

        self.assertEqual(len(layer), 6)
        self.assertEqual(len(layer.spatial['positions']), 6)

    def test_Create_3D_free_layer_from_normal_Parameter(self):
        """Test Create 3D free layer from normal parameter."""
        layer = nest.Create('iaf_psc_alpha', 7,
                            positions=nest.spatial.free(
                                nest.random.normal(dimension=3)))

        self.assertEqual(len(layer.spatial['positions']), 7)
        self.assertEqual(len(layer.spatial['positions'][0]), 3)

    def test_Create_free_layer_from_exponential_Parameter(self):
        """Test Create free layer from exponential parameter."""
        layer = nest.Create('iaf_psc_alpha', 6,
                            positions=nest.spatial.free(
                                nest.random.exponential(scale=(0.5, 1.0))))

        self.assertEqual(len(layer), 6)
        self.assertEqual(len(layer.spatial['positions']), 6)

    def test_Create_3D_free_layer_from_exponential_Parameter(self):
        """Test Create 3D free layer from exponential parameter."""
        layer = nest.Create('iaf_psc_alpha', 7,
                            positions=nest.spatial.free(
                                nest.random.exponential(dimension=3)))

        self.assertEqual(len(layer.spatial['positions']), 7)
        self.assertEqual(len(layer.spatial['positions'][0]), 3)


def suite():
    suite = unittest.makeSuite(CreateLayer, 'test')
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())

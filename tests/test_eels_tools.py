# -*- coding: utf-8 -*-
"""
Created on December 28 2021

@author: Gerd Duscher
"""
import unittest
import h5py

import sys
import os
import ase.build
import numpy as np
import sidpy
print(sidpy.__version__)
import pyTEMlib.file_tools as ft

import pyTEMlib.eels_tools as eels


class TestFileFunctions(unittest.TestCase):
    def test_dm3_eels_info(self):
        file_path = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(file_path, '../example_data/AL-DFoffset0.00.dm3')
        dataset = ft.open_file(file_name)
        dataset.h5_dataset.file.close()
        metadata = eels.read_dm3_eels_info(dataset.original_metadata)
        self.assertIsInstance(metadata, dict)
        self.assertEqual(metadata['exposure_time'], 10.0)

    def test_set_previous_quantification(self):
        file_path = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(file_path, '../example_data/AL-DFoffset0.00.dm3')
        dataset = ft.open_file(file_name)
        eels.set_previous_quantification(dataset)
        dataset.h5_dataset.file.close()

    def test_fit_peaks(self):
        file_path = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(file_path, '../example_data/AL-DFoffset0.00.dm3')
        dataset = ft.open_file(file_name)
        start_channel = np.searchsorted(dataset.energy_loss, -2)
        end_channel = np.searchsorted(dataset.energy_loss, 2)
        p = eels.fit_peaks(dataset, dataset.energy_loss.values, [[0, dataset.max(), .6]], start_channel, end_channel)
        dataset.h5_dataset.file.close()
        self.assertIsInstance(p, list)

    def test_get_x_sections(self):
        x = eels.get_x_sections()
        self.assertIsInstance(x, dict)
        self.assertEqual(len(x), 82)
        x = eels.get_x_sections(14)

        self.assertIsInstance(x, dict)
        self.assertEqual(x['name'], 'Si')

    def test_list_all_edges(self):
        z = eels.list_all_edges(14)
        self.assertEqual(z[:6], ' Si-K1')

    def test_find_major_edge(self):
        z = eels.find_major_edges(532)

        self.assertIsInstance(z, str)
        self.assertEqual(z[1:7], ' O -K1')

    def test_find_all_edge(self):
        z = eels.find_all_edges(532)
        self.assertIsInstance(z, str)
        self.assertEqual(z[1:7], ' O -K1')

    def test_second_derivative(self):
        file_path = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(file_path, '../example_data/AL-DFoffset0.00.dm3')
        dataset = ft.open_file(file_name)
        dataset.h5_dataset.file.close()

        derivative, noise_level = eels.second_derivative(dataset, 1.0)

        self.assertIsInstance(derivative, np.ndarray)

    def test_find_edges(self):
        file_path = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(file_path, '../example_data/AL-DFoffset0.00.dm3')
        dataset = ft.open_file(file_name)
        dataset.h5_dataset.file.close()

        selected_edges = eels.find_edges(dataset)

        self.assertIsInstance(selected_edges, list)

    def test_make_edges(self):
        edge = eels.make_edges(['Si-L3'], np.arange(50, 500), 200000, 20.)

        self.assertIsInstance(edge, dict)
        self.assertIsInstance(edge[0]['data'], np.ndarray)

    def test_power_law(self):
        background = eels.power_law(np.arange(50, 500), 3000., 3.)

        self.assertIsInstance(background, np.ndarray)

    def test_power_law_background(self):
        file_path = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(file_path, '../example_data/AL-DFoffset0.00.dm3')
        dataset = ft.open_file(file_name)
        dataset.h5_dataset.file.close()

        background, p = eels.power_law_background(dataset, dataset.energy_loss, [15, 25], verbose=True)

        self.assertIsInstance(background, np.ndarray)

    def test_fix_energy_scale(self):
        file_path = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(file_path, '../example_data/AL-DFoffset0.00.dm3')
        dataset = ft.open_file(file_name)

        fwhm, fit_mu = eels.fix_energy_scale(dataset, dataset.energy_loss)

        self.assertTrue(fwhm < 0.3)

    def test_resolution_function(self):
        file_path = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(file_path, '../example_data/AL-DFoffset0.00.dm3')
        dataset = ft.open_file(file_name)

        z_loss, p_zl = eels.resolution_function(dataset.energy_loss.values, np.array(dataset), 0.5, verbose=True)

        self.assertTrue(len(z_loss) == len(dataset))

    def test_get_energy_shifts(self):
        """
        file_path = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(file_path, '../example_data/AL-DFoffset0.00.dm3')
        dataset = ft.open_file(file_name)

        shifts = eels.get_energy_shifts(np.array(dataset).new_axis), dataset.energy_loss.values, 0.5)
        print(shifts)
        """

    def test_effective_collection_angle(self):
        eff_beta = eels.effective_collection_angle(np.arange(59, 500), 10, 10, 200)

        self.assertTrue(eff_beta > 10)
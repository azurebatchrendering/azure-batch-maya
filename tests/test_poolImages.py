# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os
import sys

from poolImageFilter import PoolImageFilter
from poolImageProvider import PoolImageProvider

CONTAINER_IMAGES = {
    'batchrendering/linux/maya2017:update5':
        {
            'OS': 'CentOS 73',
            'Maya': '2017-Update5',
            'ImageReference' : 'CentOS73WithContainers'
        },
    'batchrendering/linux/mtoa-maya2017:2.0.1.1':
        {
            'OS': 'CentOS 73',
            'Maya': '2017-Update5',
            'Arnold': '2.0.1.1',
            'ImageReference' : 'CentOS73WithContainers'
        },
     'batchrendering/linux/vrayformaya-maya2017:35203':
        {
            'OS': 'CentOS 73',
            'Maya': '2017-Update5',
            'VRay': '3.52.03',
            'ImageReference' : 'CentOS73WithContainers'
        },
    'batchrendering/linux/vrayformaya-maya2017:35203':
        {
            'OS': 'CentOS 73',
            'Maya': '2017-Update5',
            'VRay': '3.52.03',
            'ImageReference' : 'CentOS73WithContainers'
        },
    'dummyCombinedVrayArnold':
        {
            'OS': 'CentOS 73',
            'Maya': '2017-Update5',
            'VRay': '3.52.03',
            'Arnold': '2.0.1.1',
            'ImageReference' : 'CentOS73WithContainers'
        },

    'dummy2018-1':
        {
            'OS': 'CentOS 73',
            'Maya': '2018-Update1',
            'ImageReference' : 'CentOS73WithContainers'
        },
   'dummy2018-2':
        {
            'OS': 'CentOS 73',
            'Maya': '2018-Update1',
            'Arnold': '2.0.1.1',
            'ImageReference' : 'CentOS73WithContainers'
        },
     'dummy2018-3':
        {
            'OS': 'CentOS 73',
            'Maya': '2018-Update1',
            'VRay': '3.52.03',
            'ImageReference' : 'CentOS73WithContainers'
        },
    'dummy2018-4':
        {
            'OS': 'CentOS 73',
            'Maya': '2018-Update1',
            'VRay': '3.52.03',
            'ImageReference' : 'CentOS73WithContainers'
        },
      'dummy2018-5':
        { 
            'OS': 'CentOS 73',
            'Maya': '2018-Update1',
            'VRay': '3.52.03',
            'Arnold': '2.0.1.1',
            'ImageReference' : 'CentOS73WithContainers'
        },

     'dummyExtraVersions 1':
        {
            'OS': 'CentOS 73',
            'Maya': '2017-Update5',
            'VRay': '1.0.0.1',
            'Arnold': '1.0.0.1',
            'ImageReference' : 'CentOS73WithContainers'
        },
     'dummyExtraVersions 2':
        {
            'OS': 'CentOS 73',
            'Maya': '2017-Update5',
            'VRay': '1.0.0.1',
            'Arnold': '1.0.0.2',
            'ImageReference' : 'CentOS73WithContainers'
        },
    'dummyExtraVersions 3':
        {
            'OS': 'CentOS 73',
            'Maya': '2017-Update5',
            'VRay': '1.0.0.2',
            'Arnold': '1.0.0.1',
            'ImageReference' : 'CentOS73WithContainers'
        },
    'dummyExtraVersions 4':
        {
            'OS': 'CentOS 73',
            'Maya': '2017-Update5',
            'VRay': '1.0.0.4',
            'Arnold': '1.0.0.1',
            'ImageReference' : 'CentOS73WithContainers'
        },
    'dummyExtraVersions 5':
        {
            'OS': 'CentOS 73',
            'Maya': '2017-Update5',
            'VRay': '1.0.0.1',
            'Arnold': '1.0.0.3',
            'ImageReference' : 'CentOS73WithContainers'
        },
     'dummyWindows':
        {
            'OS': 'WindowsServer2016',
            'Maya': '2017-Update5',
            'VRay': '1.0.0.1',
            'Arnold': '1.0.0.3',
            'ImageReference' : 'Windows2016WithContainers'
        },
}



class TestPoolImages(unittest.TestCase):

    def setUp(self):
        self.poolImages = PoolImageFilter(PoolImageProvider(CONTAINER_IMAGES))
        return super(TestPoolImages, self).setUp()

#getOSDisplayList
    def testGetOSDisplayList_IncludesWindowsAndCentos73(self):
        osDisplayList = self.poolImages.getOSDisplayList()

        self.assertEqual(len(osDisplayList), 2)
        self.assertSetEqual(osDisplayList, set(['WindowsServer2016', 'CentOS 73']))

#getMayaDisplayList
    def testGetMayaDisplayList_Unfiltered_ReturnsCompleteSet(self):
        mayaDisplayList = self.poolImages.getMayaDisplayList()

        self.assertEqual(len(mayaDisplayList), 2)
        self.assertSetEqual(mayaDisplayList, set(['2018-Update1', '2017-Update5']))

    def testGetMayaDisplayList_FilteredByOS_ReturnsFilteredSet(self):
        mayaDisplayList = self.poolImages.getMayaDisplayList(selectedOS = 'WindowsServer2016')

        self.assertEqual(len(mayaDisplayList), 1)
        self.assertSetEqual(mayaDisplayList, set(['2017-Update5']))

#getVRayDisplayList
    def testGetVRayDisplayList_Unfiltered_ReturnsCompleteSet(self):
        vrayDisplayList = self.poolImages.getVrayDisplayList()

        self.assertEqual(len(vrayDisplayList), 4)
        self.assertSetEqual(vrayDisplayList, set(['3.52.03', '1.0.0.1', '1.0.0.2', '1.0.0.4']))

    def testGetVrayDisplayList_FilteredByOS_ReturnsFilteredSet(self):
        vrayDisplayList = self.poolImages.getVrayDisplayList(selectedOS = 'WindowsServer2016')

        self.assertEqual(len(vrayDisplayList), 1)
        self.assertSetEqual(vrayDisplayList, set(['1.0.0.1']))

    def testGetVrayDisplayList_FilteredByOS_AndMaya_ReturnsFilteredSet(self):
        vrayDisplayList = self.poolImages.getVrayDisplayList(selectedOS = 'CentOS 73', selectedMaya ='2018-Update1')

        self.assertEqual(len(vrayDisplayList), 1)
        self.assertSetEqual(vrayDisplayList, set(['3.52.03']))


    def testGetVrayDisplayList_FilteredByOS_AndMaya_AndArnold_ReturnsFilteredSet(self):
        vrayDisplayList = self.poolImages.getVrayDisplayList(selectedOS = 'CentOS 73', selectedMaya ='2017-Update5', selectedArnold = '1.0.0.1')

        self.assertEqual(len(vrayDisplayList), 3)
        self.assertSetEqual(vrayDisplayList, set(['1.0.0.1', '1.0.0.2', '1.0.0.4']))

#getArnoldDisplayList
    def testGetArnoldDisplayList_Unfiltered_ReturnsCompleteSet(self):
        arnoldDisplayList = self.poolImages.getArnoldDisplayList()

        self.assertEqual(len(arnoldDisplayList), 4)
        self.assertSetEqual(arnoldDisplayList, set(['2.0.1.1', '1.0.0.1', '1.0.0.2', '1.0.0.3']))

    def testGetArnoldDisplayList_FilteredByOS_ReturnsFilteredSet(self):
        arnoldDisplayList = self.poolImages.getArnoldDisplayList(selectedOS = 'WindowsServer2016')

        self.assertEqual(len(arnoldDisplayList), 1)
        self.assertSetEqual(arnoldDisplayList, set(['1.0.0.3']))

    def testGetArnoldDisplayList_FilteredByOS_AndMaya_ReturnsFilteredSet(self):
        arnoldDisplayList = self.poolImages.getArnoldDisplayList(selectedOS = 'CentOS 73', selectedMaya ='2018-Update1')

        self.assertEqual(len(arnoldDisplayList), 1)
        self.assertSetEqual(arnoldDisplayList, set(['2.0.1.1']))

    def testGetArnoldDisplayList_FilteredByOS_AndMaya_AndArnold_ReturnsFilteredSet(self):
        arnoldDisplayList = self.poolImages.getArnoldDisplayList(selectedOS = 'CentOS 73', selectedMaya ='2017-Update5', selectedVRay = '1.0.0.2')

        self.assertEqual(len(arnoldDisplayList), 1)
        self.assertSetEqual(arnoldDisplayList, set(['1.0.0.1']))

#getSelectedImage
    def testGetSelectedImage_OSMayaOnly_ReturnsFirstValidEntry(self):
        selectedImageId, selectedImage = self.poolImages.getSelectedImage(selectedOS = 'CentOS 73', selectedMaya = '2017-Update5')
        self.assertEqual(selectedImage['OS'], 'CentOS 73')

    def testGetSelectedImage_OSMayaVRay_ReturnsFirstValidEntry(self):
        selectedImageId, selectedImage = self.poolImages.getSelectedImage(selectedOS = 'CentOS 73', selectedMaya = '2017-Update5', selectedVRay = '1.0.0.2')
        self.assertEqual(selectedImage['OS'], 'CentOS 73')

    def testGetSelectedImage_OSMayaArnold_ReturnsFirstValidEntry(self):
        selectedImageId, selectedImage = self.poolImages.getSelectedImage(selectedOS = 'CentOS 73', selectedMaya = '2017-Update5', selectedArnold = '1.0.0.1')
        self.assertEqual(selectedImage['OS'], 'CentOS 73')
    

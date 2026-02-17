import unittest
from unittest.mock import patch, MagicMock
import os
import art
from simpleimage import SimpleImage
from art import get_transforms, get_images


class TestGetImages(unittest.TestCase):

    @patch("art.requests.get")  # Mock requests.get inside art module
    def test_get_images(self, mock_get):
        # 1. Configure mock response
        mock_response = MagicMock()
        mock_response.content = b"fake_image_data"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # 2. Call function with two fake URLs
        urls = ["http://fakeurl1.com/image.jpg", "http://fakeurl2.com/image.jpg"]
        get_images(urls)

        # 3. Assert requests.get was called for each URL
        self.assertEqual(mock_get.call_count, 2)
        mock_get.assert_any_call("http://fakeurl1.com/image.jpg", timeout=5)
        mock_get.assert_any_call("http://fakeurl2.com/image.jpg", timeout=5)

        # 4. Check that files were created
        self.assertTrue(os.path.exists("image1.jpg"))
        self.assertTrue(os.path.exists("image2.jpg"))

        # 5. Cleanup created files
        os.remove("image1.jpg")
        os.remove("image2.jpg")

class Test_PopArt(unittest.TestCase):

    def setUp(self):
        # Create two small test images
        self.img1 = SimpleImage.blank(2,2)
        self.img2 = SimpleImage.blank(2,2)

    def test_flip(self):
        flipped_h = self.img1.flip(0)
        flipped_v = self.img1.flip(1)
        self.assertIsInstance(flipped_h, SimpleImage)
        self.assertIsInstance(flipped_v, SimpleImage)
        self.assertEqual(flipped_h.width, self.img1.width)
        self.assertEqual(flipped_v.height, self.img1.height)

    def test_greenscreen(self):
        result = self.img1.greenscreen('red', 100, self.img2)
        self.assertIsInstance(result, SimpleImage)

    def test_blur(self):
        result = self.img1.blur()
        self.assertIsInstance(result, SimpleImage)

    def test_filter(self):
        result = self.img1.filter('red', 100)
        self.assertIsInstance(result, SimpleImage)


class Test_Art(unittest.TestCase):

    def test_build_url(self):
        url = art.build_url("1500", "1600", "flower")
        self.assertIn("q=flower", url)
        self.assertIn("dateBegin=1500", url)
        self.assertIn("dateEnd=1600", url)

    @patch("requests.get")
    def test_get_result(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"objectIDs": [10, 20, 30]}
        mock_get.return_value = mock_response

        result = art.get_result("fakeurl.com")
        self.assertEqual(result, [10, 20, 30])

    @patch("requests.get")
    def test_search_description(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"primaryImage": "img.jpg"}
        mock_get.return_value = mock_response

        urls = art.search_description([100], 1)
        self.assertEqual(urls, ["img.jpg"])

    @patch("simpleimage.SimpleImage.file")
    def test_get_transforms(self, mock_file):
        fake_img = MagicMock(spec=SimpleImage)
        fake_img.width = fake_img.height = 10
        fake_img.shrink.return_value = fake_img
        fake_img.grayscale.return_value = fake_img
        fake_img.sepia.return_value = fake_img
        fake_img.blur.return_value = fake_img
        fake_img.filter.return_value = fake_img
        fake_img.flip.return_value = fake_img
        fake_img.greenscreen.return_value = fake_img

        mock_file.return_value = fake_img

        result = art.get_transforms("a.jpg", "b.jpg")
        self.assertEqual(len(result), 12)   # Expected list length = 12

    def test_compose(self):
        img = SimpleImage.blank(10, 10)        # fake 10×10 image
        imgs = [img] * 12                      # list required by compose()

        collage = art.compose(imgs)

        self.assertEqual(collage.width, 50)    # 10 * 5 columns
        self.assertEqual(collage.height, 50)   # 10 * 5 rows
        self.assertIsInstance(collage, SimpleImage)


if __name__ == '__main__':
    unittest.main()

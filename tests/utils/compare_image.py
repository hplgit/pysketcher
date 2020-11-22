import os
from typing import Dict, Union

import numpy as np
from PIL import Image

from tests.utils import ImageComparisonFailure


def make_test_filename(file_name, purpose):
    """Make a new filename by inserting *purpose* before the file's extension."""
    base, ext = os.path.splitext(file_name)
    return "%s-%s%s" % (base, purpose, ext)


def calculate_rms(expected_image, actual_image):
    """Calculate the per-pixel errors, then compute the root mean square error."""
    if expected_image.shape != actual_image.shape:
        raise ImageComparisonFailure(
            "Image sizes do not match expected size: {} "
            "actual size {}".format(expected_image.shape, actual_image.shape)
        )
    # Convert to float to avoid overflowing finite integer types.
    return np.sqrt(((expected_image - actual_image).astype(float) ** 2).mean())


def compare_images(expected: str, actual: str, tol: float) -> Union[None, Dict]:
    """Compare two "image" files checking differences within a tolerance.

    The two given filenames may point to files which are convertible to
    PNG via the `.converter` dictionary. The underlying RMS is calculated
    with the `.calculate_rms` function.

    Args:
        expected : The filename of the expected image.
        actual : The filename of the actual image.
        tol : The tolerance (a color value difference, where 255 is the
              maximal difference).  The test fails if the average pixel
              difference is greater than this value.

    Returns:
        Return *None* if the images are equal within the given tolerance.
        If the images differ, the return value depends on  *in_decorator*.
        If *in_decorator* is true, a dict with the following entries is
        returned:
        - *rms*: The RMS of the image difference.
        - *expected*: The filename of the expected image.
        - *actual*: The filename of the actual image.
        - *diff_image*: The filename of the difference image.
        - *tol*: The comparison tolerance.

    Raises:
        ValueError: If either of the provided images is not suitable.
        IOError: If either of the image files cannot be found.

    Examples:
        >>> img1 = "docs/images/wheel_on_inclined_plane.png"
        >>> img2 = "docs/images/wheel_on_inclined_plane.png"
        >>> compare_images(img1, img2, 0.001)
    """
    actual = os.fspath(actual)
    if not os.path.exists(actual):
        raise ValueError("Output image %s does not exist." % actual)
    if os.stat(actual).st_size == 0:
        raise ValueError("Output image file %s is empty." % actual)

    # Convert the image to png
    expected = os.fspath(expected)
    if not os.path.exists(expected):
        raise IOError("Baseline image %r does not exist." % expected)

    # open the image files and remove the alpha channel (if it exists)
    expected_image = np.asarray(Image.open(expected).convert("RGB"))
    actual_image = np.asarray(Image.open(actual).convert("RGB"))

    diff_image = make_test_filename(actual, "failed-diff")

    if tol <= 0:
        if np.array_equal(expected_image, actual_image):
            return None

    # convert to signed integers, so that the images can be subtracted without
    # overflow
    expected_image = expected_image.astype(np.int16)
    actual_image = actual_image.astype(np.int16)

    rms = calculate_rms(expected_image, actual_image)

    if rms <= tol:
        return None

    save_diff_image(expected, actual, diff_image)

    results = dict(
        rms=rms,
        expected=str(expected),
        actual=str(actual),
        diff=str(diff_image),
        tol=tol,
    )

    return results


def save_diff_image(expected: str, actual: str, output: str):
    """Creates a diff image from an expected and actual image.

    Args:
        expected : File path of expected image.
        actual : File path of actual image.
        output : File path to save difference image to.

    Raises:
        ImageComparisonFailure: If the images are not compatible
    """
    # Drop alpha channels, similarly to compare_images.
    expected_image = np.asarray(Image.open(expected).convert("RGB"))
    actual_image = np.asarray(Image.open(actual).convert("RGB"))

    expected_image = np.array(expected_image).astype(float)
    actual_image = np.array(actual_image).astype(float)
    if expected_image.shape != actual_image.shape:
        raise ImageComparisonFailure(
            "Image sizes do not match expected size: {} "
            "actual size {}".format(expected_image.shape, actual_image.shape)
        )
    abs_diff_image = np.abs(expected_image - actual_image)

    # expand differences in luminance domain
    abs_diff_image *= 255 * 10
    save_image_np = np.clip(abs_diff_image, 0, 255).astype(np.uint8)
    height, width, depth = save_image_np.shape

    # The PDF renderer doesn't produce an alpha channel, but the
    # matplotlib PNG writer requires one, so expand the array
    if depth == 3:
        with_alpha = np.empty((height, width, 4), dtype=np.uint8)
        with_alpha[:, :, 0:3] = save_image_np
        save_image_np = with_alpha

    # Hard-code the alpha channel to fully solid
    save_image_np[:, :, 3] = 255

    Image.fromarray(save_image_np).save(output, format="png")

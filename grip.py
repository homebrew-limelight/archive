import grip
import cv2
import time

import inspect

CONTOUR_RETURNING_STEPS = ("find_contours", "convex_hulls", "filter_contours")

OPENCV3 = False

if cv2.__version__[0] == "3":
    OPENCV3 = True

def wrap_grip(grip_object):

    grip_class = grip_object.__class__
    filename = inspect.getfile(grip_class)

    final_line = None
    next_operator = -1

    with open(filename, "r") as file:
        for line in file:
            if next_operator > -1:
                next_operator -= 1
            if next_operator == 0:
                final_line = line
            line = line.strip().lower()
            if line.startswith("# step"):
                # only consider operator if it returns a contour
                if line.split("# step")[1].strip().startswith(CONTOUR_RETURNING_STEPS):
                    next_operator = 2

    # todo: check for final_line == None and raise error: no contour-returning step found
    final_step = final_line.strip().split()[0].split(".")[-1].split(")")[0]

    def process(mat):
        grip_object.process(mat)
        return getattr(grip_object, final_step)

    return process


# QUESTIONABLE DESIGN CHOICE EXPLANATION
# You may be wondering why we decided to use monkey patching here, and the simple answer is OpenCV compatibility.
# Currently, GRIP uses OpenCV 3. OpenCV 4 has major improvements, however it has a few API changes.
# By switching out find_contours, with a OpenCV 4 compatible version, we are able to keep performance improvements
# while still being compatible with generated GRIP code.
def find_contours(input, external_only):
    """Sets the values of pixels in a binary image to their distance to the nearest black pixel.
    Args:
        input: A numpy.ndarray.
        external_only: A boolean. If true only external contours are found.
    Return:
        A list of numpy.ndarray where each one represents a contour.
    """
    if(external_only):
        mode = cv2.RETR_EXTERNAL
    else:
        mode = cv2.RETR_LIST
    method = cv2.CHAIN_APPROX_SIMPLE
    vals = cv2.findContours(input, mode=mode, method=method)

    if OPENCV3:
        return vals[1]  # image, contours, hierarchy
    return vals[0]  # contours, hierarchy


if __name__ == "__main__":
    pipeline = grip.GripPipeline()
    pipeline._GripPipeline__find_contours = find_contours
    process = wrap_grip(pipeline)

    cap = cv2.VideoCapture(0)
    time.sleep(2)

    try:
        while True:
            ret, frame = cap.read()
            edit = process(frame)
            print(edit)
            #cv2.imshow("frame", edit)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

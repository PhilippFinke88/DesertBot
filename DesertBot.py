import warnings
import cv2
import numpy as np


def detect_edges(image):
    """
    Detects the edges of the lane in the given image.
    :param image: Image to detect lane edges in.
    :return: Greyscale image with detected lane edges.
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    filtered_image = cv2.blur(gray_image, (19, 19))
    _, binary_image = cv2.threshold(filtered_image, 150, 255, cv2.THRESH_BINARY)

    return cv2.Canny(binary_image, 200, 205)


def region_of_interest(image):
    """
    Creates a subimage of the given image with the region of interest (ROI).
    :param image: Image to extract ROI from.
    :return: 1. ROI subimage, 2. Origin of subimage relative to image.
    """
    height = image.shape[0]
    width = image.shape[1]

    y_bottom = int(height * 0.58)
    y_top = int(height * 0.39)
    x_bottom_left = int(width * 0.17)
    x_bottom_right = int(width * 0.43)
    x_top_left = int(width * 0.31)

    roi_vertices = np.array([[(x_bottom_left, y_bottom),
                              (x_bottom_right, y_bottom),
                              (x_bottom_right, y_top),
                              (x_top_left, y_top)]])

    mask = np.zeros((height, width), np.uint8)
    cv2.fillPoly(mask, roi_vertices, 255)

    return cv2.bitwise_and(image, image, mask=mask)[y_top:y_bottom, x_bottom_left:x_bottom_right], \
           (x_bottom_left, y_top)


def create_coordinates(image, lane_params):
    """
    Creates the lane's start and end coordinates in the given image
    :param image: Image where the lane has been detected in.
    :param lane_params: Lane's 1st order polynomial parameters.
    :return: Start and end coordinates of the lane in the image.
    """
    slope, intercept = lane_params

    y1 = int(image.shape[0] * 0.30)
    y2 = int(image.shape[0] * 0.65)
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)

    return np.array([x1, y1, x2, y2])


def detect_lane(image):
    """
    Detects a lane in the given image.
    :param image: Image where a lane should be detected in.
    :return: Start and end coordinates of the detected lane on success, None if no lane has been detected.
    """
    roi_image, roi_offset = region_of_interest(image)
    edge_image = detect_edges(roi_image)

    height = image.shape[0]

    lane = None
    lines = cv2.HoughLinesP(edge_image,
                            1,
                            np.pi / 180.0,
                            30,
                            minLineLength=int(height * 0.06),
                            maxLineGap=int(height * 0.1))

    if lines is not None:
        line_fit = []

        with warnings.catch_warnings():
            warnings.filterwarnings('error')

            for line in lines:
                x1, y1, x2, y2 = line.reshape(4)

                x1 += roi_offset[0]
                x2 += roi_offset[0]
                y1 += roi_offset[1]
                y2 += roi_offset[1]

                try:
                    # It will fit the polynomial and the intercept and slope
                    parameters = np.polyfit((x1, x2), (y1, y2), 1)
                    line_fit.append((parameters[0], parameters[1]))
                except np.RankWarning:
                    print('Failed to polyfit line data!')
                except:
                    print('Unknown error while polyfitting line!')

            try:
                # Compute average of all detected polynomials to get lane.
                line_fit_mean = np.mean(line_fit, axis=0)
                lane = np.array([create_coordinates(image, line_fit_mean)])
            except RuntimeWarning:
                print('Not enough data to compute lane!')
            except:
                print('Unknown error in lane detection!')

    return lane


def main():
    """
    Main function.
    """
    print("OpenCV version:" + cv2.getVersionString())

    cap = cv2.VideoCapture('examples/desertbus_screencapture.mov')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('desertbus_lane.mp4', fourcc, 60.0, (2880, 1800))

    while cap.isOpened():
        frame_ok, frame = cap.read()

        if frame_ok:
            lane = detect_lane(frame)

            if lane is not None:
                for x1, y1, x2, y2 in lane:
                    cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 10)
            else:
                print('No lane detected!')

            out.write(frame)
        else:
            print('End of video!')
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

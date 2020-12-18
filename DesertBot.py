import warnings
import cv2
import numpy as np


def detect_edges(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    filtered_image = cv2.blur(gray_image, (19, 19))
    _, binary_image = cv2.threshold(filtered_image, 150, 255, cv2.THRESH_BINARY)

    return cv2.Canny(binary_image, 200, 205)


# Filters the region of interest. In this case the yellow road marks.
def region_of_interest(image):
    height = image.shape[0]
    width = image.shape[1]
    roi_vertices = np.array([[(int(width * 0.17), int(height * 0.58)),
                              (int(width * 0.43), int(height * 0.58)),
                              (int(width * 0.43), int(height * 0.39)),
                              (int(width * 0.31), int(height * 0.39))]])

    mask = np.zeros((height, width), np.uint8)
    cv2.fillPoly(mask, roi_vertices, 255)

    return cv2.bitwise_and(image, image, mask=mask)


def create_coordinates(image, line_parameters):
    slope, intercept = line_parameters

    y1 = int(image.shape[0] * 0.30)
    y2 = int(image.shape[0] * 0.65)
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)

    return np.array([x1, y1, x2, y2])


def detect_lane(image):
    roi_image = region_of_interest(image)
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

    return lane, lines


def display_lane(image, lane):
    line_image = np.zeros_like(image)

    if lane is not None:
        for x1, y1, x2, y2 in lane:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)

    return line_image


def main():
    print("OpenCV version:" + cv2.getVersionString())

    cap = cv2.VideoCapture('examples/desertbus_screencapture.mov')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('desertbus_lane.mp4', fourcc, 60.0, (2880, 1800))

    while cap.isOpened():
        frame_ok, frame = cap.read()

        if frame_ok:
            lane = detect_lane(frame)

            if lane is not None:
                frame = cv2.addWeighted(frame, 0.8, display_lane(frame, lane), 1, 1)

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

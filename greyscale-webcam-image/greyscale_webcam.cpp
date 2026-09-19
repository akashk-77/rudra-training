#include <opencv2/opencv.hpp>
#include <iostream>

int main() {
    
    cv::VideoCapture cap(2);

    
    if (!cap.isOpened()) {
        std::cerr << "Error: Could not open the webcam." << std::endl;
        return -1;
    }

    cv::Mat frame, grayFrame;

    while (true) {
       
        cap >> frame;

        if (frame.empty()) {
            std::cerr << "Error: Captured empty frame." << std::endl;
            break;
        }

        cv::cvtColor(frame, grayFrame, cv::COLOR_BGR2GRAY);

        cv::imshow("Grayscale Webcam Feed", grayFrame);

        char key = (char)cv::waitKey(1);
        if (key == 'q' || key == 'Q' || key == 27) {
            break;
        }
    }

    cap.release();
    cv::destroyAllWindows();

    return 0;
}

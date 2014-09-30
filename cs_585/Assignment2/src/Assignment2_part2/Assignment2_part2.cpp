/**
	CS585_Assignment2.cpp
	@author:
	@version:

	CS585 Image and Video Computing Fall 2014
	Assignment 2
	--------------
	This program:
		a) Tracks an object by template matching 
		b) Recognizes hand shapes or gestures and creates a graphical display 
	--------------
	PART B
*/

#include "stdafx.h"

#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <list>
#include <Windows.h>
#pragma comment(lib, "Winmm.lib")



using namespace cv;
using namespace std;

void mySkinDetect(Mat& src, Mat& dst);
int myMax(int a, int b, int c);
int myMin(int a, int b, int c);
void myMotionEnergy(Vector<Mat> mh, Mat& dst);
void myFrameDifferencing(Mat& prev, Mat& curr, Mat& dst);
void contour(Mat& src, Mat& tmpl);
void createTemplates();
double Hausdorff(vector<Point> cont1, vector<Point> cont2);
void contour2(Mat& src);
vector<Point> templates[5];
int curValue = 0;

std::list<int> buffer;
Mat beatlesAlbum  = imread("Beatles.jpg");
Mat AmonAlbum = imread("AmonAmarth.jpg");


int main()
{

	////
	//// Create Templates
	////
	//Mat highfive = imread("highfive.jpg", CV_LOAD_IMAGE_COLOR);
	//Mat tmp = Mat::zeros(highfive.rows, highfive.cols, CV_8UC1);
	//mySkinDetect(highfive, tmp);

	//vector<Point> cc = contour(tmp);
	//templates[0] = cc; 
	//imshow( "Contours T", cc);

	VideoCapture cap(0); 

	// if not successful, exit program
    if (!cap.isOpened())  
    {
        cout << "Cannot open the video cam" << endl;
        return -1;
    }
	
	Mat frame0;

	// read a new frame from video
	bool bSuccess0 = cap.read(frame0); 


	Mat skin0 = Mat::zeros(frame0.rows, frame0.cols,CV_8UC1);
	mySkinDetect(frame0, skin0);
	//blur( skin0, skin0, Size(3,3));

	//if not successful, break loop
    if (!bSuccess0) 
	{
			cout << "Cannot read a frame from video stream" << endl;
	}

	Mat frame;
	int count = 0;
	//namedWindow("MyVideo",WINDOW_AUTOSIZE);
	while (1)
    {
		// read a new frame from video
        bool bSuccess = cap.read(frame); 
		
		//if not successful, break loop
        if (!bSuccess) 
        {
             cout << "Cannot read a frame from video stream" << endl;
             break;
        }


		imshow("Video", frame);

		Mat skin = Mat::zeros(frame.rows, frame.cols,CV_8UC1);
		mySkinDetect(frame, skin);
		//blur( skin, skin, Size(3,3));
		//imshow("Skin",skin);
		vector<vector<Point>> c;

		//contour(skin, tmp);
		contour2(skin);
		
		//resizing of template
		//double area0 = contourArea(c[0]);


		Mat frameDest;
		frameDest = Mat::zeros(frame.rows, frame.cols, CV_8UC1); //Returns a zero array of same size as src mat, and of type CV_8UC1

		//call myFrameDifferencing function
		myFrameDifferencing(skin0, skin, frameDest);

	
		if(count % 1 == 0){
			skin0 = skin.clone();
		}
		count++;

		if (waitKey(30) == 27) 
		{
			cout << "esc key is pressed by user" << endl;
			break; 
		}

	}
	
	cap.release();
	return 0;
}

//Function that detects whether a pixel belongs to the skin based on RGB values
void mySkinDetect(Mat& src, Mat& dst) {
	//Surveys of skin color modeling and detection techniques:
	//Vezhnevets, Vladimir, Vassili Sazonov, and Alla Andreeva. "A survey on pixel-based skin color detection techniques." Proc. Graphicon. Vol. 3. 2003.
	//Kakumanu, Praveen, Sokratis Makrogiannis, and Nikolaos Bourbakis. "A survey of skin-color modeling and detection methods." Pattern recognition 40.3 (2007): 1106-1122.
	for (int i = 0; i < src.rows; i++){
		for (int j = 0; j < src.cols; j++){
			//For each pixel, compute the average intensity of the 3 color channels
			Vec3b intensity = src.at<Vec3b>(i,j); //Vec3b is a vector of 3 uchar (unsigned character)
			int B = intensity[0]; int G = intensity[1]; int R = intensity[2];
			if ((R > 95 && G > 40 && B > 20) && (myMax(R,G,B) - myMin(R,G,B) > 15) && (abs(R-G) > 15) && (R > G) && (R > B)){
				dst.at<uchar>(i,j) = 255;
			}
		}
	}
}

//Function that returns the maximum of 3 integers
int myMax(int a, int b, int c) {
	int m = a;
    (void)((m < b) && (m = b)); 
    (void)((m < c) && (m = c));
     return m;
}

//Function that returns the minimum of 3 integers
int myMin(int a, int b, int c) {
	int m = a;
    (void)((m > b) && (m = b)); 
    (void)((m > c) && (m = c)); 
     return m;
}

void myMotionEnergy(Vector<Mat> mh, Mat& dst) {
	Mat mh0 = mh[0];
	Mat mh1 = mh[1];
	Mat mh2 = mh[2];

	for (int i = 0; i < dst.rows; i++){
		for (int j = 0; j < dst.cols; j++){
			if (mh0.at<uchar>(i,j) == 255 || mh1.at<uchar>(i,j) == 255 ||mh2.at<uchar>(i,j) == 255){
				dst.at<uchar>(i,j) = 255;
			}
		}
	}
}

void myFrameDifferencing(Mat& prev, Mat& curr, Mat& dst) {
	//For more information on operation with arrays: http://docs.opencv.org/modules/core/doc/operations_on_arrays.html
	//For more information on how to use background subtraction methods: http://docs.opencv.org/trunk/doc/tutorials/video/background_subtraction/background_subtraction.html
	
	//TODO:
	//Take the pixel-wise absolute difference of the previous and current frames
	//If the absolute differences are greater than a threshold, color the pixel white, else leave it black

	for (int i = 0; i < prev.rows; i++) { 
		for (int j = 0; j < prev.cols; j++) { 
			int diff = abs(prev.at<uchar>(i,j) - curr.at<uchar>(i,j));
			if (diff > 25){
				dst.at<uchar>(i,j) = 255;
			}
		}
	}

	
}

void contour2(Mat& src)
{
	vector<vector<Point>> contours;
	vector<Vec4i> hierarchy;
	findContours(src, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
	// Find largest contour
	int maxsize = 0;
	int maxind = 0;
	Rect boundrec;
	for(int i = 0; i < contours.size(); i++ )
	{
		// Documentation on contourArea: http://docs.opencv.org/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html#
		double area = contourArea(contours[i]);
		if (area > maxsize) {
			maxsize = area;
			maxind = i;
			boundrec = boundingRect(contours[i]);
		}
	}


		Mat boundCont = Mat::zeros(src.size(), CV_8UC3);
		drawContours(boundCont, contours, maxind, 	Scalar(255, 0, 0), CV_FILLED, 8, hierarchy);
		drawContours(boundCont, contours, maxind, Scalar(0,0,255), 2, 8, hierarchy);
		rectangle(boundCont, boundrec, Scalar(0,255,0),1, 8,0);
		imshow("bounded Contour", boundCont);
		cout << "height/width: " << ((double)boundrec.height)/((double)boundrec.width) <<endl;

		
		if(buffer.size() > 20){
			buffer.pop_back();
		}
		double prop = ((double)boundrec.height)/((double)boundrec.width);
		if (prop > 1.18) {
			//horns
			//cout << "horns" << endl;
			buffer.push_front(1);
		}
		
		else if (prop > .80) {
			//fist
			//cout << "fist" << endl;
			buffer.push_front(0);
		}


		else if(prop < .67) {
			//peace
			//cout << "peace" << endl;
			buffer.push_front(2);
		}

		bool matching = true;
		std::list<int>::const_iterator iterator;
		int l = *buffer.begin();
		for (iterator = buffer.begin(); iterator != buffer.end(); ++iterator) {
			if(l != *iterator){
				matching = false;
			}
		}
		if (matching && curValue != l) 
		{
			curValue = l;

			if (curValue == 0)
			{
				//Stop
				Mat pause = Mat::zeros(400,400,CV_8SC3);
				putText(pause, "Pause",Point(50,100),FONT_HERSHEY_SIMPLEX,1,Scalar(0,200,200),4);
				imshow("foo1", pause);
				

				PlaySound(NULL,0,0);
			}
			else if (curValue == 1)
			{
				//Start Slayer
				PlaySound(NULL,0,0);
				PlaySound(TEXT("AmonAmarth.wav"),NULL, SND_ASYNC);
				Mat Slayer = Mat::zeros(400,400,CV_8SC3);
				putText(AmonAlbum, "ROCK ON",Point(50,350),FONT_HERSHEY_SIMPLEX,1,Scalar(0,0,255),4);
				
				


				imshow("foo1", AmonAlbum); 
				//imshow("foo1", Slayer);

			}
			else if (curValue == 2)
			{
				//Start Beatles 
				PlaySound(NULL,0,0);
				PlaySound(TEXT("Beatles.wav"),NULL, SND_ASYNC);
				
				Mat beatles = Mat::zeros(400,400,CV_8SC3);
				putText(beatlesAlbum, "BEATLES",Point(50,30),FONT_HERSHEY_SIMPLEX,1,Scalar(0,255,0),4);
				
				imshow("foo1", beatlesAlbum);
				//imshow("foo1", beatles);
				
			}

			cout << "Value is : " << l << endl;
		}


}

/**
* Finds contours of frame and template and then attempts either Hasudorff or averaging
*/
void contour(Mat& src, Mat& tmpl)
{

	


	vector<vector<Point>> contours;
	vector<Vec4i> hierarchy;
	// Find contours
	// Documentation for finding contours: http://docs.opencv.org/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html?highlight=findcontours#findcontours
	findContours(src, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );

	//Mat contour_output = Mat::zeros( src.size(), CV_8UC3 );
	//cout << "The number of contours detected is: " <<  contours.size() << endl;

	// Find largest contour
	int maxsize = 0;
	int maxind = 0;
	Rect boundrec;
	for(int i = 0; i < contours.size(); i++ )
	{
		// Documentation on contourArea: http://docs.opencv.org/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html#
		double area = contourArea(contours[i]);
		if (area > maxsize) {
			maxsize = area;
			maxind = i;
			boundrec = boundingRect(contours[i]);
		}
	}

	Mat boundCont = Mat::zeros(src.size(), CV_8UC3);

	if(contours.size() > 0){

		drawContours(boundCont, contours, maxind, 	Scalar(255, 0, 0), CV_FILLED, 8, hierarchy);
		drawContours(boundCont, contours, maxind, Scalar(0,0,255), 2, 8, hierarchy);
		rectangle(boundCont, boundrec, Scalar(0,255,0),1, 8,0);

		imshow("bounded Contour", boundCont);


		Mat justContour = Mat::zeros(boundrec.height, boundrec.width, CV_8UC3);
		int csize = contours[maxind].size();
		vector<Point> shiftContour;
		std::vector<Point>::iterator shiftIt;
		std::vector<Point>::iterator origIt;
		shiftIt = shiftContour.begin();

	
		for (unsigned i = 0; i < contours[maxind].size(); i++)
		{
			Point temp = contours[maxind].at(i);
			temp.x = temp.x - boundrec.x;
			temp.y = temp.y - boundrec.y;
		
			contours[maxind].at(i) = Point(temp.x,temp.y);
			
		}
	
		// Draw contours
		// Documentation for drawing contours: http://docs.opencv.org/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html?highlight=drawcontours#drawcontours
		drawContours(justContour, contours, maxind, Scalar(255, 0, 0), CV_FILLED, 8, hierarchy);
		drawContours(justContour, contours, maxind, Scalar(0,0,255), 2, 8, hierarchy);
		// Documentation for drawing rectangle: http://docs.opencv.org/modules/core/doc/drawing_functions.html
		//rectangle(contour_output, boundrec, Scalar(0,255,0),1, 8,0);
	
		//imshow("Shifted", justContour);

		resize(tmpl, tmpl, boundrec.size());
		vector<vector<Point>> contours_t;
		vector<Vec4i> hierarchy_t;
		findContours(src, contours_t, hierarchy_t, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
		int maxsize_t = 0;
		int maxind_t = 0;
		Rect boundrec_t;
		for(int i = 0; i < contours_t.size(); i++ )
		{
			// Documentation on contourArea: http://docs.opencv.org/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html#
			double area_t = contourArea(contours_t[i]);
			if (area_t > maxsize_t) {
				maxsize_t = area_t;
				maxind_t = i;
				boundrec_t = boundingRect(contours_t[i]);
			}
		}

		cout << "Hausdorff: "<<  Hausdorff(contours[maxind], contours_t[maxind_t]) << endl;


	}
	//cout << "The area of the largest contour detected is: " <<  contourArea(contours[maxind]) << endl;
	//cout << "-----------------------------" << endl << endl;

	/// Show in a window
	//namedWindow( "Contours", CV_WINDOW_AUTOSIZE );
	//imshow( "Contours", contour_output);
	//return contour_output;
}

double Hausdorff(vector<Point> cont1, vector<Point> cont2)
{
	//cont1 -> cont2
	int min1 = 100000;
	int min2 = 100000;
	int distance1 = 0;
	int distance2 = 0;
	int count1 = 0;
	int count2 = 0;
	for(int i = 0; i < cont1.size(); i++)
	{
		
		for (int j = 0; j < cont2.size(); j++) {
			int xdist = abs( cont1.at(i).x - cont2.at(j).x); 
			int ydist = abs( cont1.at(i).y - cont2.at(j).y);
			distance1 += xdist + ydist;
			count1++;

			
		}
		
	}

	for(int i = 0; i < cont2.size(); i++)
	{
		
		for (int j = 0; j < cont1.size(); j++) {
			int xdist = abs( cont1.at(j).x - cont2.at(i).x); 
			int ydist = abs( cont1.at(j).y - cont2.at(i).y);
			distance2 += xdist + ydist;
			count2++;
			
		}
		
	}

	return (distance1 + distance2) /(count1 + count2); 

}


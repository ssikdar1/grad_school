/**
	CS585_Assignment2.cpp
	@author: Shan Sikdar and Sweek
	@version: 1 

	CS585 Image and Video Computing Fall 2014
	Assignment 2
	--------------
	This program:
		a) Tracks an object by template matching 
		b) Recognizes hand shapes or gestures and creates a graphical display 
	--------------
	PART A
*/

#include "stdafx.h"

#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>



using namespace cv;
using namespace std;

int myRotate(Mat& src, Mat& dst);
int orientation = 1;


int main()
{
	//getTemplate();
	try
	{
		Mat result;
		Mat tmpl = imread("charlieCard.jpeg", CV_LOAD_IMAGE_COLOR);
		Mat tmpl2,tmpl3,tmpl4;
		myRotate(tmpl,tmpl2);
		myRotate(tmpl2,tmpl3);
		myRotate(tmpl3, tmpl4);

		Mat templates[] = {tmpl,tmpl2,tmpl3,tmpl4};

		imshow("Template", tmpl);

		VideoCapture cap(0); 
		// if not successful, exit program
		if (!cap.isOpened())  
		{
			cout << "Cannot open the video cam" << endl;
			return -1;
		}
	

		Mat frame;
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

			int method =  CV_TM_CCORR_NORMED;
			
			Mat tmp1;
			Mat tmp2;
			pyrDown(frame,tmp1,Size( frame.cols/2, frame.rows/2 ));
			

			double minVal; double maxVal; Point minLoc; Point maxLoc;
			Point matchLoc;


			double max_r = -3;
			int index = 0;
			
			if(orientation == 1)
			{
				for ( int i = 0; i < 4; i++)
				{

					matchTemplate( frame, templates[i], result, method);
					minMaxLoc( result, &minVal, &maxVal, &minLoc, &maxLoc, Mat() );
					//cout << "maxVal" << maxVal <<endl;
					if(maxVal > max_r)
					{
						max_r = maxVal;
						matchLoc = maxLoc;
						index = i;
						//cout << "index" << index <<endl;
					}
					
				}
			}else{
				matchTemplate( frame, templates[index], result, method);
				minMaxLoc( result, &minVal, &maxVal, &minLoc, &maxLoc, Mat() );
				matchLoc = maxLoc;
			}

			/// Show me what you got
			rectangle( frame, matchLoc, Point( matchLoc.x + templates[index].cols , matchLoc.y + templates[index].rows ), Scalar::all(225), 2, 8, 0 );
			rectangle( result, matchLoc, Point( matchLoc.x + templates[index].cols , matchLoc.y + templates[index].rows ), Scalar::all(255), 2, 8, 0 );

			imshow("MyVideo", frame);
			imshow("Result", result);

			int c;
			c = waitKey(10);

			/*if (waitKey(30) == 27) 
			{
				cout << "esc key is pressed by user" << endl;
				break; 
			}*/

			if( (char)c == 'u' )
			{ 
				Mat tmp = templates[index].clone();
				pyrUp( tmp, templates[index], Size( tmp.cols*2, tmp.rows*2 ) );
				printf( "** Zoom In: Image x 2 \n" );
			}

			if( (char)c == 'h' )
			{ 
				Mat tmp2 = templates[index].clone();
				pyrDown( tmp2, templates[index], Size( tmp2.cols/2, tmp2.rows/2 ) );
				printf( "** Zoom Out: Image x 2 \n" );
			}

		}
		cap.release();

	}catch(int e){
		cout << "Exepction e: " << e << endl;
		getchar();
	}
		return 0;
}

int myRotate(Mat& src, Mat& dst)
{
	// Rotate the image
		//myRotate(90,tmpl);
		//Mat tmpl2 = tmpl.clone();

		transpose(src, dst);
		flip(dst,dst,0);
		return 0;
	/*
	int iScale = 50;
	int iBorderMode = 0;
	int iImageCenterY = img.rows/2;
	int iImageCenterX = img.cols/2;
	const char* pzRotatedImage = "Rotated Image";

	 Mat matRotation = getRotationMatrix2D(  Point( iImageCenterX, iImageCenterY ), (iAngle - 180), iScale / 50.0 );

	warpAffine( img, img, matRotation, img.size(), INTER_LINEAR, iBorderMode, Scalar() );

	return 0;*/
}


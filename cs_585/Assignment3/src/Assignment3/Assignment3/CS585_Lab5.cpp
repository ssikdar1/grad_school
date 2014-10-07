/**
*/

#include "stdafx.h"
#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <algorithm> // for sort

using namespace cv;
using namespace std;

//Global variables
int thresh = 215;//220;
int thresh2 = 230;
int max_thresh = 255;
Mat src; Mat src_gray;
vector<Point> globalContours[5];

Mat binaryFold(Mat img3);
Mat doubleThreshold(Mat src_gray);
Mat findContours(Mat src, int a);

double calcCircularity(Moments m);
Mat skeleton(Mat img);

int myMax(int a, int b, int c);
int myMin(int a, int b, int c);
void mySkinDetect(Mat& src, Mat& dst);
void q1_2();
void q3();
void q4();
void q5();


	int morph_elem = 0;
	int morph_size = 1;
	int morph_operator = 0;
	int const max_operator = 4;
	int const max_elem = 2;
	int const max_kernel_size = 21;

	Mat element = getStructuringElement( morph_elem, Size( 2*morph_size + 1, 2*morph_size+1 ), Point( morph_size, morph_size ) );



// Semi Database Go Go Jagoob
struct image_Props{
	double area;
	double perimeter;
	double compactness;
	double orientation;
	double circularity;
	int holes;

};

image_Props details[5];


// main function
int main()
{


	//q1_2();
	//q3();
	//q4();  // run q1_2() to generate values for struct
	//q5();

	

	waitKey(0);
	return(0);
}

void q1_2()
{
	Mat src1 = imread("bcancer1.png", 1);
	Mat src2 = imread("bcancer2.png", 1);
	Mat src3 = imread("bcancer3.png", 1);
	Mat src4 = imread("bcancer4.png", 1);
	Mat tmp[] = {src1, src2, src3, src4};

	int morph_elem = 0;
	int morph_size = 1;
	int morph_operator = 0;
	int const max_operator = 4;
	int const max_elem = 2;
	int const max_kernel_size = 21;
	vector <vector<Point2i>> blobs;

	Mat element = getStructuringElement( morph_elem, Size( 2*morph_size + 1, 2*morph_size+1 ), Point( morph_size, morph_size ) );


	namedWindow("Source", CV_WINDOW_AUTOSIZE );
	Mat threshed[4];

	for(int i = 0; i < 4 ; i++){
		 // Convert image to gray
		//imshow( "Source" + i, src_gray );

		cvtColor( tmp[i], src_gray, CV_BGR2GRAY );
		threshed[i] = doubleThreshold(src_gray);
		
//		imshow("After double" + std::to_string(i), threshed[i]);
	
		morphologyEx( threshed[i], threshed[i], MORPH_CLOSE, element ); /// Apply the specified morphology operation
		
		//imshow("after morph" + std::to_string(i), threshed[i]);

		morphologyEx( threshed[i], threshed[i], MORPH_CLOSE, element ); /// Apply the specified morphology operation

		//imshow("after morph2" + std::to_string(i), threshed[i]);

		//find largest contour
		
		Mat contour_output = findContours(threshed[i], i);

		Mat contour_outputRev = contour_output == 0;

		//imshow( "Contours"+ std::to_string(i), contour_outputRev);

		details[i].perimeter = globalContours[i].size();
		details[i].area = contourArea(globalContours[i]);

		details[i].compactness = (details[i].perimeter * details[i].perimeter)/details[i].area;
		
		
		//Moments
		Moments mom = moments( globalContours[i], true ); 
	
		details[i].orientation = .5*atan((2*mom.mu11)/(mom.mu20 - mom.mu02));
		cout << "orientation" << i << " : "<< details[i].orientation << endl;

		details[i].circularity = calcCircularity(mom);

	

		cout << "Image " << i << " p,a,c,h,circ "<< details[i].perimeter << " , " << details[i].area << " , " << details[i].compactness << ", "<< blobs.size() << " , " << details[i].circularity <<endl;


	}
}

void q3()
{
	Mat img1 = imread("bcancer3.3.png", 1);
	Mat img2 = imread("bcancer2.1.png", 1);
	Mat img3 = imread("bcancer2.2.png", 1);
	Mat img4 = imread("bcancer3.1.png", 1);
	Mat img5 = imread("bcancer3.2.png", 1);
	
	Mat folds[] = {img1,img2,img3,img4,img5};
	Mat foldResults[5];
	for (int i = 0; i < 5; i++)  
	{
		foldResults[i] = binaryFold(folds[i]);

		imshow("fold: " + std::to_string(i), foldResults[i]);

		imshow("foldResults: " + std::to_string(i), skeleton(foldResults[i]));

		

	}

	
}


void q4()
{
	Mat lost_image = imread("bcancer4.png",1);
	imshow("LOST IMAGE", lost_image);
	
	Mat src1 = imread("bcancer1.png", 1);
	Mat src2 = imread("bcancer2.png", 1);
	Mat src3 = imread("bcancer3.png", 1);
	Mat src4 = imread("bcancer4.png", 1);
	Mat tmp[] = {src1, src2, src3, src4};

	
	// CALCULATE VALUE FOR LOST IMAGE

		cvtColor( lost_image, src_gray, CV_BGR2GRAY );
		lost_image = doubleThreshold(src_gray);
		
		//imshow("After double" + std::to_string(i), threshed[i]);
	
		morphologyEx( lost_image, lost_image, MORPH_CLOSE, element ); /// Apply the specified morphology operation
		
		//imshow("after morph" + std::to_string(i), threshed[i]);

		morphologyEx( lost_image, lost_image, MORPH_CLOSE, element ); /// Apply the specified morphology operation

		//imshow("after morph2" + std::to_string(i), threshed[i]);

		//find largest contour
		
		Mat contour_output = findContours(lost_image, 4);

		Mat contour_outputRev = contour_output == 0;

		//imshow( "Contours"+ std::to_string(i), contour_outputRev);

		details[4].perimeter = globalContours[4].size();
		details[4].area = contourArea(globalContours[4]);

		details[4].compactness = (details[4].perimeter *details[4].perimeter)/details[4].area;
		
		
		//Moments
		Moments mom = moments( globalContours[4], true ); 
	
		details[4].orientation = .5*atan((2*mom.mu11)/(mom.mu20 - mom.mu02));
		cout << "Lost Image orientation" << 4 << " : "<< details[4].orientation << endl;

		details[4].circularity = calcCircularity(mom);
		double similarity;
		double min = 9999999999999999999;
		int minIndex = 0;
		for ( int a = 0; a < 4;  a++)
		{
			similarity =  abs(details[a].circularity - details[4].circularity) + abs(details[a].compactness- details[4].compactness) + abs(details[a].holes - details[4].holes) + abs(details[a].orientation - details[4].orientation);
			if(similarity < min)
			{
				min = similarity;
				minIndex = a;
				

			}
			cout << a << " Similarity: " << similarity << endl;

		}
		
		cout<< "BEST COMPARISON IS " << minIndex << endl;
		imshow("BEST MATCH", tmp[minIndex]);

}


void q5()
{
	Mat broken_image = imread("broken_Slide.png",1);
	imshow("BROKEN IMAGE", broken_image);
	
	Mat src1 = imread("bcancer1.png", 1);
	Mat src2 = imread("bcancer2.png", 1);
	Mat src3 = imread("bcancer3.png", 1);
	Mat src4 = imread("bcancer4.png", 1);
	Mat tmp[] = {src1, src2, src3, src4};

	Mat result;
	//double normVals[4];
	int index=0;
	int maxMatch = -2;
		double minVal; double maxVal;
		Point minLoc; Point maxLoc;
	for( int i =0; i < 4; i++)
	{
		//resize(broken_image, broken_image, tmp[i].size()); // IN REAL LIFE MESSED UP SHIT Yo, Ajjen
		matchTemplate(tmp[i], broken_image, result, CV_TM_CCORR_NORMED );				
		minMaxLoc( result, &minVal, &maxVal, &minLoc, &maxLoc, Mat() );
		//normVals[i]= maxVal;	

		if(maxVal > maxMatch)
		{
			maxMatch = maxVal;
			index = i;
		}
	}

	//sort(normVals, normVals+4);  // Generalize 4 to array length

	cout<<"BEST MATCH IS :"<< index << " With Norm Value: "<<maxMatch <<endl;
	imshow("ANSWER TEMPLATE MATCH", tmp[index]);

}


Mat skeleton(Mat img)
{
	//http://felix.abecassis.me/2011/09/opencv-morphological-skeleton/
	
	//Mat img;
	threshold(img, img, 127, 255, THRESH_BINARY);
	Mat skel(img.size(), CV_8UC1, Scalar(0));
	Mat temp(img.size(), CV_8UC1);
	Mat element = getStructuringElement(MORPH_CROSS, Size(3, 3));

	bool done;
	do
	{
	  morphologyEx(img, temp, MORPH_OPEN, element);
	  bitwise_not(temp, temp);
	  bitwise_and(img, temp, temp);
	  bitwise_or(skel, temp, skel);
	  erode(img, img, element);
 
	  double max;
	  minMaxLoc(img, 0, &max);
	  done = (max == 0);
	} while (!done);

	return skel;
}


void mySkinDetect(Mat& src, Mat& dst) {
	//Surveys of skin color modeling and detection techniques:
	//Vezhnevets, Vladimir, Vassili Sazonov, and Alla Andreeva. "A survey on pixel-based skin color detection techniques." Proc. Graphicon. Vol. 3. 2003.
	//Kakumanu, Praveen, Sokratis Makrogiannis, and Nikolaos Bourbakis. "A survey of skin-color modeling and detection methods." Pattern recognition 40.3 (2007): 1106-1122.
	for (int i = 0; i < src.rows; i++){
		for (int j = 0; j < src.cols; j++){
			//For each pixel, compute the average intensity of the 3 color channels
			Vec3b intensity = src.at<Vec3b>(i,j); //Vec3b is a vector of 3 uchar (unsigned character)
			int B = intensity[0]; int G = intensity[1]; int R = intensity[2];
			int Ravg = 186;
			int delta = 45;
			//if (!((R > 186 && G > 60 && B > 50) && (myMax(R,G,B) - myMin(R,G,B) > 15) && (abs(R-G) > 15) && (R > G) && (R > B))){
			//if(R < 210 && R > 140 && G> 20 && G <95 && B < 155 && B > 80){
				if( R < Ravg + delta  && R > Ravg- delta  && (myMax(R,G,B) - myMin(R,G,B) > 15) && (abs(R-G) > 15) && (R > G) && (R > B)){
					dst.at<uchar>(i,j) = 255;
				}
			//}
			//}
		}
	}
}

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


Mat doubleThreshold(Mat src)
{
	Mat thres_output1;
	Mat thres_output2;
	thres_output1 = src < thresh;
	thres_output2 = src < thresh2;

	Mat threshoutput = Mat::zeros(Size(src.cols, src.rows), thres_output1.type());

	for(int j = 0; j < thres_output1.cols; j++)
	{
		for (int i = 0; i < thres_output1.rows; i++)
		{
			uchar pixel1 = thres_output1.at<uchar>(i,j);
			uchar pixel2 = thres_output2.at<uchar>(i,j);



			if(pixel1 == 255)
			{
				threshoutput.at<uchar>(i,j) = 255;
			}
			else if (pixel2 == 0){
				threshoutput.at<uchar>(i,j) = 0;
			}
			else if(pixel1 == 0 && pixel2 == 255 && i < src.rows - 1 && j < src.cols - 1 && i > 0 && j > 0)
			{

				//cout << "i,j  " << i << " , " << j << endl;

				if (thres_output1.at<uchar>(i-1, j) == 255 || thres_output1.at<uchar>(i + 1, j) || thres_output1.at<uchar>(i, j - 1) || thres_output1.at<uchar>(i, j + 1))
				{
					threshoutput.at<uchar>(i,j) = 255;
				}



				else
				{
					threshoutput.at<uchar>(i,j) = 0;
				}

			}
			else
			{
				threshoutput.at<uchar>(i,j) = 0;
			}


		}
	}

	//threshold( src_gray, thres_output1, thresh, max_thresh,THRESH_BINARY_INV);
	//imshow("thres 1", thres_output1);
	//imshow("thres 2", thres_output2);
	//imshow("Double Thresh", threshoutput);

	return threshoutput;


}

Mat findContours(Mat src, int a)
{

	Mat thres_output;
	vector<vector<Point>> contours;
	vector<Vec4i> hierarchy;
	
	// Find contours
	// Documentation for finding contours: http://docs.opencv.org/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html?highlight=findcontours#findcontours
	findContours(src, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );

	Mat contour_output = Mat::zeros( src.size(), CV_8UC3 );
	cout << "The number of contours detected is: " <<  contours.size() << endl;

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
	
	// Draw contours
	// Documentation for drawing contours: http://docs.opencv.org/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html?highlight=drawcontours#drawcontours
	drawContours(contour_output, contours, maxind, 	Scalar(255, 255, 255), CV_FILLED, 8, hierarchy);
	drawContours(contour_output, contours, maxind, Scalar(255,255,255), 2, 8, hierarchy);

	//contour_output = contour_output == 0;
	// Documentation for drawing rectangle: http://docs.opencv.org/modules/core/doc/drawing_functions.html
	//rectangle(contour_output, boundrec, Scalar(0,255,0),1, 8,0);

	//cout << "The area of the largest contour detected is: " <<  contourArea(contours[maxind]) << endl;
	//cout << "-----------------------------" << endl << endl;

	/// Show in a window
	//namedWindow( "Contours", CV_WINDOW_AUTOSIZE );
	//imshow( "Contours", contour_output);
	globalContours[a] = contours[maxind];

	//Find Holes:
	int holes = 0;
	for(vector<Vec4i>::size_type idx=0; idx<hierarchy.size(); ++idx)
    {
        if(hierarchy[idx][3] != -1)
           holes++;
    }
	details[a].holes = holes;
	cout << "Holes "<< a << ": " <<  details[a].holes;


	return contour_output;
}

double calcCircularity(Moments m)
{
	double a = m.mu20;
	double b = m.mu11;
	double c = m.mu02;
	double e_min = (a + c)*.5 - (a - c)*.5*((a-c)/sqrt((a-c)*(a-c)+b*b)) -b*.5*(b/sqrt((a-c)*(a-c)+b*b));
	double e_max = (a + c)*.5 - (a - c)*.5*(-(a-c)/sqrt((a-c)*(a-c)+b*b))-b*.5*(-b/sqrt((a-c)*(a-c)+b*b));
	return e_min/e_max;
}


Mat binaryFold(Mat img3){


	Mat dst = Mat::zeros(img3.size(), CV_8UC1);
	
	Mat temp;
	img3.copyTo(temp);
	
	cvtColor( img3, img3, CV_BGR2GRAY );
	GaussianBlur(img3, img3, Size(5,5), 5) ;
	imshow("Blurred", img3);
	adaptiveThreshold(img3, dst, 255, ADAPTIVE_THRESH_MEAN_C, THRESH_BINARY_INV,301, -1);

	//morphologyEx( dst, dst, MORPH_OPEN, element );
	
	for(int i = 0; i < temp.rows; i++){
		for(int j = 0; j < temp.cols; j++){
			if(dst.at<uchar>(i,j) != 255 ){
				temp.at<Vec3b>(i,j) = (0,0,0);
			}
		}
	}
	Mat dst2 = Mat::zeros(temp.size(), CV_8UC1);
	//mySkinDetect(temp,dst2);
	dst2 = dst;
	//dst2 = dst2 == 0;
	morphologyEx( dst2, dst2, MORPH_CLOSE, element ); /// Apply the specified morphology operation
	//	morphologyEx( dst2, dst2, MORPH_CLOSE, element ); /// Apply the specified morphology operation
		
	erode(dst2,dst2,element);
	erode(dst2,dst2,element);

	//imshow("skel test", dst2);

	Mat thres_output;
	vector<vector<Point>> contours;
	vector<Vec4i> hierarchy;

	findContours(dst2, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );

	Mat contour_output = Mat::zeros( dst2.size(), CV_8UC3 );
	cout << "The number of contours detected is: " <<  contours.size() << endl;

	dst2.copyTo(contour_output);
	/*for(int i = 0; i < contours.size(); i++ )
	{
		// Documentation on contourArea: http://docs.opencv.org/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html#
		double area = contourArea(contours[i]);
		if (area > 75) {
			drawContours(contour_output, contours, i, 	Scalar(255, 255, 255), CV_FILLED, 8, hierarchy);
			drawContours(contour_output, contours, i, Scalar(255,255,255), 2, 8, hierarchy);
		}
	}
	*/
	element = getStructuringElement( morph_elem, Size( 2*morph_size + 2, 2*morph_size+2), Point( morph_size, morph_size ) );

	morphologyEx(contour_output, contour_output, MORPH_CLOSE, element );
	
	erode(contour_output, contour_output, element);

	erode(contour_output, contour_output, element);
	morphologyEx(contour_output, contour_output, MORPH_CLOSE, element );

	vector<vector<Point>> contours2;
	vector<Vec4i> hierarchy2;

	Mat cont2 = Mat::zeros(contour_output.size(), contour_output.type());


	findContours(dst2, contours2, hierarchy2, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
	for(int i = 0; i < contours2.size(); i++ )
	{
		// Documentation on contourArea: http://docs.opencv.org/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html#
		double area = contourArea(contours2[i]);
		if (area > .025*((double)(img3.rows * img3.cols))) {
			drawContours(cont2, contours2, i, 	Scalar(255, 255, 255), CV_FILLED, 8, hierarchy2);
			drawContours(cont2, contours2, i, Scalar(255,255,255), 2, 8, hierarchy2);
		}
	}
	
	
	return cont2;
}

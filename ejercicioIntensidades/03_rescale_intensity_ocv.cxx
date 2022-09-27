#include <stdio.h>
#include <opencv2/opencv.hpp>

using namespace cv;

int main(int argc, char** argv )
{
  // Get command line arguments
  if ( argc < 3 )
  {
  	std::cerr << "Usage: " << argv[ 0 ] << " image_file number_of_bits" << std::endl;
    return( -1 );

  } // fi

  // Review given command line arguments
  std::cout << "-------------------------" << std::endl;
  for( int a = 0; a < argc; a++ )
    std::cout << argv[ a ] << std::endl;
  std::cout << "-------------------------" << std::endl;

  // Read an image
  Mat image;
  image = imread( argv[1], 1 );

  if ( !image.data )
  {
    std::cerr << "Error: No image data" << std::endl;
    return( -1);
  }

  // Convert RGB image to grayscale
  Mat gray_image;
  cvtColor( image, gray_image, COLOR_BGR2GRAY );

  // Create color channel images
  // red channel
  Mat rImg = Mat::zeros( image.size( ), CV_8UC1 );
  // green channel
  Mat gImg = Mat::zeros( image.size( ), CV_8UC1 );

  // blue channel
  Mat bImg = Mat::zeros( image.size( ), CV_8UC1 );

  // composite image (RGB)
  Mat rgbImg = Mat::zeros( image.size( ), CV_8UC3 );

  // Fill color channel images
  MatIterator_< Vec3b > it, rgbIt, diffIt, end, endrgb, enddiff;
  MatIterator_< uchar > crIt, cgIt, cbIt, endr, endg, endb;
  it = image.begin< Vec3b >( );
  crIt = rImg.begin< uchar >( );
  cgIt = gImg.begin< uchar >( );
  cbIt = bImg.begin< uchar >( );
  end = image.end< Vec3b >( );
  endr = rImg.end< uchar >( );
  endg = gImg.end< uchar >( );
  endb = bImg.end< uchar >( );
  for(  ; it != end, crIt != endr, cgIt != endg, cbIt != endb; ++it, ++crIt, ++cgIt, ++cbIt)
  {
    (*crIt) = (*it)[2];
    (*cgIt) = (*it)[1];
    (*cbIt) = (*it)[0];

  } // rof




  // Quantize into desired number of bits
  uchar table[ 256 ];
  int scale = pow( 2, 8 - atoi( argv[ 2 ] ) );
  for (int i = 0; i < 256; ++i)
    table[ i ] = ( uchar )( scale * ( i / scale ) );

  Mat resint_img = Mat::zeros( image.size( ), CV_8UC1 );
  MatIterator_< uchar > it0, end0;
  for( it0 = resint_img.begin< uchar >( ), end0 = resint_img.end< uchar >( ); it0 != end0; ++it0)
    *it0 = table[*it0];

  // Quantize color channels
  //Red
  Mat resint_imgR = Mat::zeros( image.size( ), CV_8UC1 );
  MatIterator_< uchar > it2, end1;
  for( it0 = resint_imgR.begin< uchar >( ), end0 = resint_imgR.end< uchar >( ); it0 != end0; ++it0)
    *it0 = table[*it0];

  //Green
  Mat resint_imgG = Mat::zeros( image.size( ), CV_8UC1 );
  MatIterator_< uchar > it3, end2;
  for( it3 = resint_imgG.begin< uchar >( ), end2 = resint_imgG.end< uchar >( ); it3 != end2; ++it3)
    *it3 = table[*it3];

  //Blue
  Mat resint_imgB = Mat::zeros( image.size( ), CV_8UC1 );
  MatIterator_< uchar > it4, end3;
  for( it4 = resint_imgB.begin< uchar >( ), end3 = resint_imgB.end< uchar >( ); it4 != end3; ++it4)
    *it4 = table[*it4];

  // Rescale intensities to cover the full range
  Mat lookUpTable(1, 256, CV_8U);
  uchar* p = lookUpTable.data;
  for( int i = 0; i < 256; ++i)
    p[i] = table[i];
  LUT(gray_image, lookUpTable, resint_img);
  
  LUT(rImg, lookUpTable, resint_imgR);
  LUT(gImg, lookUpTable, resint_imgG);
  LUT(bImg, lookUpTable, resint_imgB);

  // From color channel images, reconstruct the color image
  crIt = resint_imgR.begin< uchar >( );
  cgIt = resint_imgG.begin< uchar >( );
  cbIt = resint_imgB.begin< uchar >( );
  rgbIt = rgbImg.begin< Vec3b >( );
  endr = resint_imgR.end< uchar >( );
  endg = resint_imgG.end< uchar >( );
  endb = resint_imgB.end< uchar >( );
  endrgb = rgbImg.end< Vec3b >( );
  for(  ; crIt != endr, cgIt != endg, cbIt != endb, rgbIt != endrgb; ++crIt, ++cgIt, ++cbIt, ++rgbIt)
  {
    (*rgbIt)[0] = (*cbIt);
    (*rgbIt)[1] = (*cgIt);
    (*rgbIt)[2] = (*crIt);
    
  } // rof
  

  // Write results
  std::stringstream ss( argv[ 1 ] );
  std::string basename;
  getline( ss, basename, '.' );

  imwrite( basename + "_intensity.png", gray_image );
  imwrite( basename + "_rescaleInt.png", resint_img );

  
  imwrite( basename + "_rescaleIntRED.png", resint_imgR );
  imwrite( basename + "_rescaleIntGREEN.png", resint_imgG );
  imwrite( basename + "_rescaleIntBLUE.png", resint_imgB );
  imwrite( basename + "_finalRGB.png", rgbImg );
  

  return( 0 );
}

// eof - 02_rescale_intensity.cxx

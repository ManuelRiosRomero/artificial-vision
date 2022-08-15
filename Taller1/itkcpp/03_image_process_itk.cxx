#include <cmath>
#include <cstdlib>
#include <limits>
#include <iostream>
#include <string>
#include <sstream>

#include <itkImage.h>
#include <itkRGBPixel.h>

#include <itkImageFileReader.h>
#include <itkImageFileWriter.h>

#include <itkImageRegionConstIteratorWithIndex.h>
#include <itkImageRegionIteratorWithIndex.h>
#include <itkIdentityTransform.h>
#include <itkResampleImageFilter.h>

#include <itkSubtractImageFilter.h>
#include "itkSubtractImageFilter.h"
//#include <itkImageToVTKImageFilter.h>

// Image type: 2-dimensional 1-byte rgb
const unsigned int Dim = 2;
typedef unsigned char TRGBResolution;
typedef itk::RGBPixel<TRGBResolution> TRGBPixel;
typedef itk::Image<TRGBPixel, Dim> TColorImage;

// Types definition
typedef itk::ImageFileReader<TColorImage> TReader;
typedef itk::ImageRegionConstIteratorWithIndex<TColorImage> TIterator;
typedef itk::ImageRegionIteratorWithIndex<TColorImage> TColorIterator;
typedef itk::ImageFileWriter<TColorImage> TWriter;
typedef itk::IdentityTransform<double, 2> TransformType;
typedef itk::ResampleImageFilter<TColorImage, TColorImage> ResampleImageFilterType;

// -------------------------------------------------------------------------
int main(int argc, char *argv[])
{
  // Get command line arguments
  if (argc < 2)
  {
    std::cerr << "Usage: " << argv[0] << " image_file" << std::endl;
    return (-1);

  } // fi

  // Review given command line arguments
  std::cout << "-------------------------" << std::endl;
  for (int a = 0; a < argc; a++)
    std::cout << argv[a] << std::endl;
  std::cout << "-------------------------" << std::endl;

  // Read an image
  TReader::Pointer reader = TReader::New();
  reader->SetFileName(argv[1]);
  try
  {
    reader->Update();
  }
  catch (itk::ExceptionObject &err)
  {
    std::cerr << "Error: " << err << std::endl;
    return (1);

  } // yrt
  TColorImage *img = reader->GetOutput();

  // Create color channel images
  // red channel
  TColorImage::Pointer rImg = TColorImage::New();
  rImg->SetSpacing(img->GetSpacing());
  rImg->SetOrigin(img->GetOrigin());
  rImg->SetLargestPossibleRegion(img->GetLargestPossibleRegion());
  rImg->SetRequestedRegion(img->GetRequestedRegion());
  rImg->SetBufferedRegion(img->GetBufferedRegion());
  rImg->Allocate();

  // green channel
  TColorImage::Pointer gImg = TColorImage::New();
  gImg->SetSpacing(img->GetSpacing());
  gImg->SetOrigin(img->GetOrigin());
  gImg->SetLargestPossibleRegion(img->GetLargestPossibleRegion());
  gImg->SetRequestedRegion(img->GetRequestedRegion());
  gImg->SetBufferedRegion(img->GetBufferedRegion());
  gImg->Allocate();

  // blue channel
  TColorImage::Pointer bImg = TColorImage::New();
  bImg->SetSpacing(img->GetSpacing());
  bImg->SetOrigin(img->GetOrigin());
  bImg->SetLargestPossibleRegion(img->GetLargestPossibleRegion());
  bImg->SetRequestedRegion(img->GetRequestedRegion());
  bImg->SetBufferedRegion(img->GetBufferedRegion());
  bImg->Allocate();

  // composite image (RGB)
  TColorImage::Pointer rgbImg = TColorImage::New();
  rgbImg->SetSpacing(img->GetSpacing());
  rgbImg->SetOrigin(img->GetOrigin());
  rgbImg->SetLargestPossibleRegion(img->GetLargestPossibleRegion());
  rgbImg->SetRequestedRegion(img->GetRequestedRegion());
  rgbImg->SetBufferedRegion(img->GetBufferedRegion());
  rgbImg->Allocate();

  // Initialize created images in black
  TRGBPixel black;
  black.SetRed(0);
  black.SetGreen(0);
  black.SetBlue(0);
  rImg->FillBuffer(black);
  gImg->FillBuffer(black);
  bImg->FillBuffer(black);
  rgbImg->FillBuffer(black);

  // Fill color channel images
  TIterator it(img, img->GetLargestPossibleRegion());
  TColorIterator crIt(rImg, rImg->GetLargestPossibleRegion());
  TColorIterator cgIt(gImg, gImg->GetLargestPossibleRegion());
  TColorIterator cbIt(bImg, bImg->GetLargestPossibleRegion());

  it.GoToBegin();
  crIt.GoToBegin();
  cgIt.GoToBegin();
  cbIt.GoToBegin();
  for (; !it.IsAtEnd() && !crIt.IsAtEnd() && !cgIt.IsAtEnd() && !cbIt.IsAtEnd(); ++it, ++crIt, ++cgIt, ++cbIt)
  {
    TRGBPixel value, pixel;
    pixel = it.Get();
    value.SetRed(pixel.GetRed());
    value.SetGreen(0);
    value.SetBlue(0);
    crIt.Set(value);

    value.SetRed(0);
    value.SetGreen(pixel.GetGreen());
    value.SetBlue(0);
    cgIt.Set(value);

    value.SetRed(0);
    value.SetGreen(0);
    value.SetBlue(pixel.GetBlue());
    cbIt.Set(value);

  } // rof

  // Write results
  std::stringstream ss(argv[1]);
  std::string basename;
  getline(ss, basename, '.');

  TWriter::Pointer writer = TWriter::New();
  writer->SetInput(rImg);
  std::string fotoRed = basename + "_R.png";
  writer->SetFileName(fotoRed);
  try
  {
    writer->Update();
  }
  catch (itk::ExceptionObject &err)
  {
    std::cerr << "Error: " << err << std::endl;
    return (1);

  } // yrt

  writer->SetInput(gImg);
  std::string fotoGreen = basename + "_G.png";
  writer->SetFileName(fotoGreen);
  try
  {
    writer->Update();
  }
  catch (itk::ExceptionObject &err)
  {
    std::cerr << "Error: " << err << std::endl;
    return (1);

  } // yrt

  writer->SetInput(bImg);
  std::string fotoBlue = basename + "_B.png";
  writer->SetFileName(fotoBlue);
  try
  {
    writer->Update();
  }
  catch (itk::ExceptionObject &err)
  {
    std::cerr << "Error: " << err << std::endl;
    return (1);

  } // yrt

  // ----------------- Crear Escalado de imagene Roja ----------------------
  // Read an image
  reader->SetFileName(fotoRed);
  try
  {
    reader->Update();
  }
  catch (itk::ExceptionObject &err)
  {
    std::cerr << "Error: " << err << std::endl;
    return (1);

  } // yrt
  TColorImage *RSimg = reader->GetOutput();
  TColorImage::SizeType inputSize = RSimg->GetLargestPossibleRegion().GetSize();
  TColorImage::SizeType OriginalInputSize = RSimg->GetLargestPossibleRegion().GetSize();

  std::cout << "Red Image input size: " << inputSize << std::endl;

  // Calculate output size and scaling
  TColorImage::SizeType outputSize;
  outputSize[0] = inputSize[0] * 0.75;
  outputSize[1] = inputSize[1] * 0.75;

  std::cout << "Red Image output size: " << outputSize << std::endl;

  TColorImage::SpacingType outputSpacing;
  TColorImage::SpacingType OriginalOutputSpacing;

  OriginalOutputSpacing[0] = RSimg->GetSpacing()[0];
  OriginalOutputSpacing[1] = RSimg->GetSpacing()[1];

  outputSpacing[0] =
      RSimg->GetSpacing()[0] * (static_cast<double>(inputSize[0]) / static_cast<double>(outputSize[0]));
  outputSpacing[1] =
      RSimg->GetSpacing()[1] * (static_cast<double>(inputSize[1]) / static_cast<double>(outputSize[1]));

  // Rescale image
  ResampleImageFilterType::Pointer resampleFilter = ResampleImageFilterType::New();
  resampleFilter->SetTransform(TransformType::New());
  resampleFilter->SetInput(RSimg);
  resampleFilter->SetSize(outputSize);
  resampleFilter->SetOutputSpacing(outputSpacing);
  resampleFilter->UpdateLargestPossibleRegion();

  // Write results
  std::string reducedFotoRed = basename + "_sR.png";

  writer = TWriter::New();
  writer->SetInput(resampleFilter->GetOutput());
  writer->SetFileName(reducedFotoRed);
  try
  {
    writer->Update();
  }
  catch (itk::ExceptionObject &err)
  {
    std::cerr << "Error: " << err << std::endl;
    return (1);

  } // yrt

  // ----------------- Crear Escalado de imagene Azul ----------------------
  // Read an image
  reader = TReader::New();
  reader->SetFileName(fotoBlue);
  try
  {
    reader->Update();
  }
  catch (itk::ExceptionObject &err)
  {
    std::cerr << "Error: " << err << std::endl;
    return (1);

  } // yrt
  TColorImage *BSimg = reader->GetOutput();
  inputSize = BSimg->GetLargestPossibleRegion().GetSize();

  std::cout << "Blue Image input size: " << inputSize << std::endl;

  // Calculate output size and scaling
  outputSize;
  outputSize[0] = inputSize[0] * 0.25;
  outputSize[1] = inputSize[1] * 0.25;

  std::cout << "Blue Image output size: " << outputSize << std::endl;

  outputSpacing;
  outputSpacing[0] =
      BSimg->GetSpacing()[0] * (static_cast<double>(inputSize[0]) / static_cast<double>(outputSize[0]));
  outputSpacing[1] =
      BSimg->GetSpacing()[1] * (static_cast<double>(inputSize[1]) / static_cast<double>(outputSize[1]));

  // Rescale image
  resampleFilter = ResampleImageFilterType::New();
  resampleFilter->SetTransform(TransformType::New());
  resampleFilter->SetInput(BSimg);
  resampleFilter->SetSize(outputSize);
  resampleFilter->SetOutputSpacing(outputSpacing);
  resampleFilter->UpdateLargestPossibleRegion();

  // Write results
  std::string reducedFotoBlue = basename + "_sB.png";

  writer = TWriter::New();
  writer->SetInput(resampleFilter->GetOutput());
  writer->SetFileName(reducedFotoBlue);
  try
  {
    writer->Update();
  }
  catch (itk::ExceptionObject &err)
  {
    std::cerr << "Error: " << err << std::endl;
    return (1);

  } // yrt

  // ----------------- Crear Escalado de imagene Verde ----------------------
  // Read an image
  reader->SetFileName(fotoGreen);
  try
  {
    reader->Update();
  }
  catch (itk::ExceptionObject &err)
  {
    std::cerr << "Error: " << err << std::endl;
    return (1);

  } // yrt
  TColorImage *GSimg = reader->GetOutput();
  inputSize = GSimg->GetLargestPossibleRegion().GetSize();

  std::cout << "Green Image input size: " << inputSize << std::endl;

  // Calculate output size and scaling
  // TColorImage::SizeType outputSize;
  outputSize[0] = inputSize[0] * 0.50;
  outputSize[1] = inputSize[1] * 0.50;

  std::cout << "Green Image output size: " << outputSize << std::endl;

  // TColorImage::SpacingType outputSpacing;
  outputSpacing[0] =
      GSimg->GetSpacing()[0] * (static_cast<double>(inputSize[0]) / static_cast<double>(outputSize[0]));
  outputSpacing[1] =
      GSimg->GetSpacing()[1] * (static_cast<double>(inputSize[1]) / static_cast<double>(outputSize[1]));

  // Rescale image
  // ResampleImageFilterType::Pointer resampleFilter = ResampleImageFilterType::New();
  resampleFilter->SetTransform(TransformType::New());
  resampleFilter->SetInput(GSimg);
  resampleFilter->SetSize(outputSize);
  resampleFilter->SetOutputSpacing(outputSpacing);
  resampleFilter->UpdateLargestPossibleRegion();

  // Write results
  std::string reducedFotoGreen = basename + "_sG.png";

  writer = TWriter::New();
  writer->SetInput(resampleFilter->GetOutput());
  writer->SetFileName(reducedFotoGreen);
  try
  {
    writer->Update();
  }
  catch (itk::ExceptionObject &err)
  {
    std::cerr << "Error: " << err << std::endl;
    return (1);

  } // yrt

  std::cout << "----Imagenes De Escaladas----" << std::endl;
  // ----------------------Re Escalar imagen Roja---------------------

  // Read an image
  TReader::Pointer ReReader = TReader::New();
  ReReader->SetFileName(reducedFotoRed);
  try
  {
    ReReader->Update();
  }
  catch (itk::ExceptionObject &err)
  {
    std::cerr << "Error: " << err << std::endl;
    return (1);

  } // yrt
  TColorImage *RSSimg = ReReader->GetOutput();
  TColorImage::SizeType inputSizeRss = RSSimg->GetLargestPossibleRegion().GetSize();

  std::cout << "Rescaled Red Image input size: " << inputSizeRss << std::endl;

  // Calculate output size and scaling
  outputSize;
  outputSize = OriginalInputSize;
  // outputSize[1] = OriginalInputSize;

  std::cout << "Rescaled Red Image output size: " << outputSize << std::endl;

  outputSpacing;
  outputSpacing = OriginalOutputSpacing;
  // Rescale image
  resampleFilter = ResampleImageFilterType::New();
  resampleFilter->SetTransform(TransformType::New());
  resampleFilter->SetInput(RSSimg);
  resampleFilter->SetSize(outputSize);
  resampleFilter->SetOutputSpacing(outputSpacing);
  resampleFilter->UpdateLargestPossibleRegion();

  // Write results
  std::string increasedFotoRed = basename + "_ssR.png";

  writer = TWriter::New();
  TColorImage::Pointer RedFinal = TColorImage::New();
  RedFinal = resampleFilter->GetOutput();
  writer->SetInput(RedFinal);
  writer->SetFileName(increasedFotoRed);
  try
  {
    writer->Update();
  }
  catch (itk::ExceptionObject &err)
  {
    std::cerr << "Error: " << err << std::endl;
    return (1);

  } // yrt

  // ----------------------Re Escalar imagen Azul---------------------

  // Read an image
  TReader::Pointer ReReaderB = TReader::New();
  ReReaderB->SetFileName(reducedFotoBlue);
  try
  {
    ReReaderB->Update();
  }
  catch (itk::ExceptionObject &err)
  {
    std::cerr << "Error: " << err << std::endl;
    return (1);

  } // yrt
  TColorImage *BSSimg = ReReaderB->GetOutput();
  TColorImage::SizeType inputSizeBss = BSSimg->GetLargestPossibleRegion().GetSize();

  std::cout << "Rescaled Blue Image input size: " << inputSizeBss << std::endl;

  // Calculate output size and scaling
  outputSize;
  outputSize = OriginalInputSize;

  std::cout << "Rescaled Blue Image output size: " << outputSize << std::endl;

  outputSpacing;
  outputSpacing = OriginalOutputSpacing;

  // Rescale image
  resampleFilter = ResampleImageFilterType::New();
  resampleFilter->SetTransform(TransformType::New());
  resampleFilter->SetInput(BSSimg);
  resampleFilter->SetSize(outputSize);
  resampleFilter->SetOutputSpacing(outputSpacing);
  resampleFilter->UpdateLargestPossibleRegion();

  // Write results
  std::string increasedFotoBlue = basename + "_ssB.png";

  writer = TWriter::New();
  TColorImage::Pointer BlueFinal = TColorImage::New();
  BlueFinal = resampleFilter->GetOutput();
  writer->SetInput(BlueFinal);
  writer->SetFileName(increasedFotoBlue);
  try
  {
    writer->Update();
  }
  catch (itk::ExceptionObject &err)
  {
    std::cerr << "Error: " << err << std::endl;
    return (1);

  } // yrt

  // ----------------------Re Escalar imagen Verde---------------------

  // Read an image
  TReader::Pointer ReReaderG = TReader::New();
  ReReaderG->SetFileName(reducedFotoGreen);
  try
  {
    ReReaderG->Update();
  }
  catch (itk::ExceptionObject &err)
  {
    std::cerr << "Error: " << err << std::endl;
    return (1);

  } // yrt
  TColorImage *GSSimg = ReReaderG->GetOutput();
  TColorImage::SizeType inputSizeGss = GSSimg->GetLargestPossibleRegion().GetSize();

  std::cout << "Rescaled Green Image input size: " << inputSizeGss << std::endl;

  // Calculate output size and scaling
  outputSize;
  outputSize = OriginalInputSize;

  std::cout << "Rescaled Green Image output size: " << outputSize << std::endl;

  outputSpacing;
  outputSpacing = OriginalOutputSpacing;

  // Rescale image
  resampleFilter = ResampleImageFilterType::New();
  resampleFilter->SetTransform(TransformType::New());
  resampleFilter->SetInput(GSSimg);
  resampleFilter->SetSize(outputSize);
  resampleFilter->SetOutputSpacing(outputSpacing);
  resampleFilter->UpdateLargestPossibleRegion();

  // Write results
  std::string increasedFotoGreen = basename + "_ssG.png";

  writer = TWriter::New();
  TColorImage::Pointer GreenFinal = TColorImage::New();
  GreenFinal = resampleFilter->GetOutput();
  writer->SetInput(GreenFinal);

  writer->SetFileName(increasedFotoGreen);
  try
  {
    writer->Update();
  }
  catch (itk::ExceptionObject &err)
  {
    std::cerr << "Error: " << err << std::endl;
    return (1);

  } // yrt

  // ---------------RECONSTRUIR IMAGEN-------------------

  // Initialize created images in black

  /*
  black.SetRed( 0 );
  black.SetGreen( 0 );
  black.SetBlue( 0 );
  RSSimg->FillBuffer( black );
  GSSimg->FillBuffer( black );
  BSSimg->FillBuffer( black );
  rgbImg->FillBuffer( black );
  */
  ;
  TColorIterator cRssIt(RedFinal, RedFinal->GetLargestPossibleRegion());

  TColorIterator cGssIt(GreenFinal, GreenFinal->GetLargestPossibleRegion());

  TColorIterator cBssIt(BlueFinal, BlueFinal->GetLargestPossibleRegion());

  // From color channel images, reconstruct the original color image
  TColorIterator rgbIt(rgbImg, rgbImg->GetLargestPossibleRegion());

  rgbIt.GoToBegin();
  cRssIt.GoToBegin();
  cGssIt.GoToBegin();
  cBssIt.GoToBegin();

  for (; !rgbIt.IsAtEnd() && !cRssIt.IsAtEnd() && !cGssIt.IsAtEnd() && !cBssIt.IsAtEnd(); ++rgbIt, ++cRssIt, ++cGssIt, ++cBssIt)
  {
    // std::cout<<"\n prueba: "<<prueba<<std::endl;
    TRGBPixel value, pixel;
    value = cRssIt.Get();
    pixel.SetRed(value.GetRed());

    value = cGssIt.Get();
    pixel.SetGreen(value.GetGreen());

    value = cBssIt.Get();
    pixel.SetBlue(value.GetBlue());

    rgbIt.Set(pixel);

  } // rof

  writer->SetInput(rgbImg);
  writer->SetFileName(basename + "_rRGB.png");
  try
  {
    writer->Update();
  }
  catch (itk::ExceptionObject &err)
  {
    std::cerr << "Error: " << err << std::endl;
    return (1);

  } // yrt

  //----------Comparacion de las 2 Imagenes--------------------
    
    TColorImage::Pointer diff = TColorImage::New();
    diff->SetSpacing(img->GetSpacing());
    diff->SetOrigin(img->GetOrigin());
    diff->SetLargestPossibleRegion(img->GetLargestPossibleRegion()) ;
    diff->SetRequestedRegion(img->GetRequestedRegion());
    diff->SetBufferedRegion(img->GetBufferedRegion());
    diff->Allocate();

    TColorIterator ogIt(img, img->GetLargestPossibleRegion());
    TColorIterator reconstruidaIt(rgbImg, rgbImg->GetLargestPossibleRegion());
    TColorIterator diffIT(diff, diff->GetLargestPossibleRegion());

    ogIt.GoToBegin();
    reconstruidaIt.GoToBegin();
    diffIT.GoToBegin();

    for (; !reconstruidaIt.IsAtEnd() && !diffIT.IsAtEnd() && !ogIt.IsAtEnd() ; ++reconstruidaIt, ++diffIT, ++ogIt)
    {

      TRGBPixel value, og, rgbP;
      og = ogIt.Get();
      rgbP = reconstruidaIt.Get();
      value.SetRed(og.GetRed() - rgbP.GetRed());
      value.SetGreen(og.GetGreen() - rgbP.GetGreen());
      value.SetBlue(og.GetBlue() - rgbP.GetBlue());
      diffIT.Set(value);

    } // rof
  
  writer->SetInput(diff);
  writer->SetFileName(basename + "_diff.png");
  try
  {
    writer->Update();
  }
  catch (itk::ExceptionObject &err)
  {
    std::cerr << "Error: " << err << std::endl;
    return (1);

  } // yrt

  return (0);
}
// ////////////////////// Reconstruccion de la Imagen///////////////////////////////
// eof - 01_color_channels.cxx

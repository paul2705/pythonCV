import ImgRegistration

XMLFileName='../PCVBook/PCVBookData/jkfaces.xml';
Points=ImgRegistration.ReadPointsFromXML(XMLFileName);

ImgRegistration.RigidAlignment(Points,'../PCVBook/PCVBookData/jkfaces');

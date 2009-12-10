/*
 *  DataFile.h
 *  DataFileIndexer
 *
 *  Created by David Cox on 8/17/09.
 *  Copyright 2009 Harvard University. All rights reserved.
 *
 */

#ifndef PYTHON_DATA_BINDINGS_H_
#define PYTHON_DATA_BINDINGS_H_


#include "PythonDataBindingsHelpers.h"

#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/register_ptr_to_python.hpp>

using namespace boost;
using namespace boost::python;



// Create a module called "_data"; a pure python module ("data") will load this and add some
// more pythonic fixin's on top
BOOST_PYTHON_MODULE(_data)
{
    
    PyEval_InitThreads();
 
    //def("convert_scarab_to_python", convert_scarab_to_python, "Convert a Scarab datum to a corresponding Python object, recursing as needed");

    
    class_<EventWrapper, boost::noncopyable>("Event", init<ScarabDatum *>())
    .add_property("code", &EventWrapper::getEventCode)
    .add_property("time", &EventWrapper::getTime)
    .add_property("value", extract_event_value)
    .add_property("empty", &EventWrapper::empty)
    ;
    
    register_ptr_to_python< shared_ptr<EventWrapper> >();
    
    class_<std::vector<EventWrapper> >("EventWrapperArray")
        .def(vector_indexing_suite< std::vector<EventWrapper> >())
    ;
    
    class_< std::vector<unsigned int> >("unsigned_int_vector")
        .def(vector_indexing_suite< std::vector<unsigned int> >())
    ;
    
    class_<PythonDataFile>("MWKFile", init<std::string>())
        .def("open", &PythonDataFile::open)
        .def("close", &PythonDataFile::close)
        .def("__fetch_all_events", &PythonDataFile::fetch_all_events)
        .def("__fetch_events", &PythonDataFile::fetch_events1)
        .def("__fetch_events", &PythonDataFile::fetch_events2)
        .def("__fetch_events", &PythonDataFile::fetch_events3)
        .def("__test_function", &PythonDataFile::test_function)
        .add_property("exists", &PythonDataFile::exists)
        .add_property("loaded", &PythonDataFile::loaded)
        .add_property("valid", &PythonDataFile::valid)
        .add_property("minimum_time", &PythonDataFile::minimum_time)
        .add_property("maximum_time", &PythonDataFile::maximum_time)
        .add_property("file", &PythonDataFile::file)
        .add_property("true_mwk_file", &PythonDataFile::true_mwk_file)
        ;
    
    
    class_<PythonDataStream>("MWKStream", init<std::string>())
        .def("open", &PythonDataStream::open)
        .def("close", &PythonDataStream::close)
        .def("__read_event", &PythonDataStream::read_event)
        ;
    
}

#endif
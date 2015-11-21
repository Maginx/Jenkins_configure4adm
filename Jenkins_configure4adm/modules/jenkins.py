# -*- coding: UTF-8 -*-
import os
import base64, urllib2
import json
import re
import socket
import sys
import warnings
from shell import run_shell
from errors import JenkinsException

class Jenkins(object):
    '''Jenkins class using urllib2
    '''
    _BUILD_JOB = 'job/%(job_name)s/build'
    _JENKINS_JOB_INFO = 'job/%(job_name)s/api/json?depth=0'
    _CONFIG_JOB = 'job/%(job_name)s/config.xml'
    _JENKINS_CREATE_JOB = 'createItem?name=%(job_name)s'
    def __init__(self, url, user, password):
        '''Initial jenkins class
        @param url : jenkins url, string
        @param user : jenkins user, string
        @param password : corresponding password, string
        '''
        self.__user = user
        self.__token = password
        self._url = url
        if not self._url[-1] == '/':
            self._url = url + '/'
        self._auth = 'Basic ' + base64.encodestring('%s:%s' % (self.__user, self.__token)).replace('\n', '')

    def __open_jenkins(self, request):
        try:
            if self._auth:
                request.add_header('Authorization', self._auth)
                return urllib2.urlopen(request).read()
        except urllib2.HTTPError, e:
            if e.code in [401, 403, 500]:
                raise JenkinsException(e)
            print(e)
        except urllib2.URLError, e:
            raise JenkinsException(e)

    def job_exists(self, job_name):
        '''
        @param job_name: Name of Jenkins job
        @type  job_name: str
        @return: True if Jenkins job exists
        '''
        try:
            self.get_job(job_name)
            return True
        except JenkinsException,e:
            print("ERROR ")
            print(e)
            return False

    def create_job(self, job_name, config_xml):
        '''create jenkins job with config xml file.
        '''
        if not os.path.exists(config_xml):
            raise JenkinsException("can't find file %s" % config_xml)

        with open(config_xml) as xml:
            data = xml.read()
            if self.job_exists(job_name):
                raise JenkinsException('job [%s] already exists'%(job_name))
            headers = {'Content-Type': 'text/xml'}
            reconfig_url = self._url + self._JENKINS_CREATE_JOB % locals()
            print self._url + "job/" + job_name
            self.__open_jenkins(urllib2.Request(reconfig_url, data, headers))
            if not self.job_exists(job_name):
                raise JenkinsException('create[%s] failed'%(job_name))
            return True

    def reconfig_job(self, job_name, config_xml):
        '''Change configuration of existing Jenkins job.

        To create a new job, see :meth:`Jenkins.create_job`.

        @param name: Name of Jenkins job, ``str``
        @param config_xml: New XML configuration, ``str``
        '''
        headers = {'Content-Type': 'text/xml'}
        reconfig_url = self._url + self._CONFIG_JOB % locals()
        self.__open_jenkins(urllib2.Request(reconfig_url, config_xml, headers))
        return True



    def delete_job(self, job_name):
        '''delete jenkins job
        '''
        auth_req = urllib2.Request("%sjob/%s/doDelete" % (self._url, job_name), "")
        return self.__open_jenkins(auth_req)

    def get_job(self, job_name):
        '''Get jenkins job json format data
        @param job_name : jenkins job name
        @return : json object
        @exception : JenkinsException
        '''
        try:
            response = self.__open_jenkins(urllib2.Request(self._url + self._JENKINS_JOB_INFO%locals()))
            if response:
                return json.loads(response)
            else:
                raise JenkinsException('job[%s] does not exist'%job_name)
        except ValueError,e:
            raise JenkinsException(e)

    def get_job_xml(self, job_name):
        '''Get jenkins job xml format file
        @param job_name : jenkins job name,string
        @return : xml file content, string
        @exception : JenkinsException
        '''
        try:
            response = self.__open_jenkins(urllib2.Request(self._url + self._CONFIG_JOB % locals()))
            if response:
                return response
            else:
                raise JenkinsException('job[%s] does not exist'%job_name)
        except JenkinsException, e:
            print("ERROR")
            print(e)
            return None

    def build(self, job_name):
        '''
        @param parameters: parameters for job, or None.
        @type  parameters: dict
        '''
        if not self.job_exists(job_name):
            raise JenkinsException('no such job[%s]'%(job_name))
        return self.__open_jenkins(urllib2.Request(self._url + self._BUILD_JOB % locals()))

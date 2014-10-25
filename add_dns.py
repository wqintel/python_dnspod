#!/usr/bin/env python
#-*- coding:utf-8 -*-

from dnspod.apicn import *

class dnsPod(object):
    def __init__(self):
        self.email = ""
        self.password = ""
        self.mydomain = "mydomain.com"

        if not self.email and not self.password:
            assert 0

    def get_domain_id(self,domain,*args):
        ''' *args : 域名的信息参数 '''
        get_api = DomainList(email=self.email, password=self.password)
        data    = get_api()
        domains = data.get('domains')
        for name in domains:
            if name.get('name') == domain:
                domain_id = name.get('id')

        argList = []

        if args:
            for arg in args:
                argList.append(name.get(arg,0))
            return domain_id,argList
        else:
            return domain_id

    def get_record_id(self,domain,sub_domain):
        domain_id = self.get_domain_id(domain)
        api = RecordList(domain_id, email=self.email, password=self.password)
        records = api().get('records')

        for r in records:
            if r.get('name') == sub_domain:
                return r.get('id')

    def change(self):
        '''
        change dns record
             
        '''
        pass

    def set(self,domain,name,type,line,value,ttl=300):
        '''
        set dns record  
             name      : "s1.game"
             type      : A   CNAME  TXT  NS  AAAA  MX   URL   SRV  
             line      : 默认, 电信, 联通    
             value     : ip
             ttl       : 300
             domain_id : 
             email     : user
             password  : pwd

             example   : set('mydomain.com',"testdnsapi.world", "A", u'默认', '1.1.1.1')
                         set('mydomain.com','s12.game','CNAME',u'默认','world.mydomain.com.')

        '''
        domain_id = self.get_domain_id(domain)

        assert  domain_id

        print 'domain_id: ',domain_id
        api = RecordCreate(name, type, line.encode("utf8"), value, ttl, domain_id=domain_id, email=self.email, password=self.password)

        record = api().get("record", {})
        #record_id = record.get("id")

        return record
        
        
    def delete(self,domain,sub_domain):
        ''' 
            return code example: {u'status': {u'message': u'Action completed successful', u'code': u'1', u'created_at': u'2012-10-19 13:20:32'}} 

            example            : delete('mydomain.com',"testdnsapi.world"
        '''

        domain_id = get_domain_id(domain)
        record_id = get_record_id(domain,sub_domain)

        api = RecordRemove(domain_id ,record_id,email=self.email, password=self.password)

        try:
            code = api()
        except Exception:
            pass

        mark = code.get('status').get('code')
        if mark  == '1':
            print("Delete record %s is OK"%sub_domain)
            return True
        else:
            print("Delete record %s is Failure"%sub_domain)
            return mark


    def get_all_record(self,domain,format=False):
        '''
            example   :   get_all_record('mydomain.com')

        '''
        domain_id = self.get_domain_id(domain)
        api = RecordList(domain_id, email=self.email, password=self.password)

        records = api().get('records')

        for i in records:
            if not format:
                print i.get('name'),i.get('value'),i.get('type'),i.get('line')
            else:
                print '%-25s'%i.get('name') ,'=>','%-15s'%i.get('value'),'=>','%-5s'%i.get('type'),'=>',"mx: %-5s"%i.get('mx'),'=>', '%-5s'%i.get('line')

        print "All Record : %s"%len(records)

if __name__ == '__main__':
    dns = dnsPod()
    dns.get_all_record('mydomain.com')

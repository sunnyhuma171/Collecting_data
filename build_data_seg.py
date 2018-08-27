# -*- coding: utf-8 -*-

from PyNLPIR import * 


if __name__ == '__main__':
    if init('C:\python-nlpir-master', Constants.CodeType.UTF8_CODE):
        print 'NLPIR initialization succeed.'
    else:
        raise 'NLPIR initialization fail.'
    speed = file_process('./high_quality.pos', './high_quality_seg.pos', False)
    if speed:
        print 'Processing speed: %f words/s' % speed
    else:
        print 'Processing failed.'
    speed1 = file_process('./low_quality.neg', './low_quality_seg.neg', False)
    if speed1:
        print 'Processing speed1: %f words/s' % speed1
    else:
        print 'Processing failed.'
    exit()
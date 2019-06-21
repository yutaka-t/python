# -*- coding:utf-8 -*-
import fureai_scraping as fp

if __name__ == '__main__':
    b_list = fp.load_temporarily_list()

    fp.output_booking_list(b_list)

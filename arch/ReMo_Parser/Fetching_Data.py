#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import urllib2
import json

sw = " === "

b_data = {}
error_urls = []

y = """
    <table class="offer_table narrow_offer_table checkbox_panel" >
                  <thead>
                    <tr>
                      <th colspan="4">Standard wykończeń</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td class="margin_column"></td>
                      <td class="table_field_label"><span class = "inactive_table_field">tryskacze</span></td>
                      <td class="table_field_label"><span>czujniki dymu i ciepła</span></td>
                      <td class="margin_column"></td>
                    </tr>
                    <tr>
                      <td class="margin_column"></td>
                      <td class="table_field_label"><span>podwójne zasilanie</span></td>
                      <td class="table_field_label"><span class = "inactive_table_field">podnoszone podłogi</span></td>
                      <td class="margin_column"></td>
                    </tr>
                    <tr>
                      <td class="margin_column"></td>
                      <td class="table_field_label"><span>kontrola dostępu</span></td>
                      <td class="table_field_label"><span>podwieszane sufity</span></td>
                      <td class="margin_column"></td>
                    </tr>
                    <tr>
                      <td class="margin_column"></td>
                      <td class="table_field_label"><span>okablowanie telefoniczne</span></td>
                      <td class="table_field_label"><span>wykładziny</span></td>
                      <td class="margin_column"></td>
                    </tr>
                    <tr>
                      <td class="margin_column"></td>
                      <td class="table_field_label"><span>okablowanie komputerowe</span></td>
                      <td class="table_field_label"><span>otwierane okna</span></td>
                      <td class="margin_column"></td>
                    </tr>
                    <tr>
                      <td class="margin_column"></td>
                      <td class="table_field_label"><span>okablowanie elektryczne</span></td>
                      <td class="table_field_label"><span>łącze światłowodowe</span></td>
                      <td class="margin_column"></td>
                    </tr>
                    <tr>
                      <td class="margin_column"></td>
                      <td class="table_field_label"><span>centrala telefoniczna</span></td>
                      <td class="table_field_label"><span>ścianki działowe</span></td>
                      <td class="margin_column"></td>
                    </tr>
                    <tr>
                      <td class="margin_column"></td>
                      <td class="table_field_label"><span>klimatyzacja</span></td>
                      <td class="table_field_label"><span class = "inactive_table_field">BMS</span></td>
                      <td class="margin_column"></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div id="available_areas_header">
              <div id="available_areas_header_label">
                Dostępne powierzchnie
              </div>
            </div>
            <div id="available_areas">
              <table class="building_space_table" id="building_space_table_0">
                <tr class="building_header">
                  <th></th>
                  <th class="building_header_label" colspan="5">BUDYNEK A</th>
                  <th class="building_header_label" colspan="5">BUDYNEK B</th>
                  <th class="building_header_label" colspan="4">BUDYNEK C</th>
                </tr>
                <tr class="building_subheader building_first_subheader">
                  <th class="floor_no"></th>
                  <th class="total_space">CAŁK. POW. m<sup>2</sup></th>
                  <th class="available_space_top_label" colspan="3">DOSTĘPNE POWIERZCHNIE</th>
                  <th rowspan="2" class="combine"><span>ŁĄCZENIE</span></th>
                  <th class="total_space">CAŁK. POW. m<sup>2</sup></th>
                  <th class="available_space_top_label" colspan="3">DOSTĘPNE POWIERZCHNIE</th>
                  <th rowspan="2" class="combine"><span>ŁĄCZENIE</span></th>
                  <th class="total_space">CAŁK. POW. m<sup>2</sup></th>
                  <th class="available_space_top_label" colspan="3">DOSTĘPNE POWIERZCHNIE</th>
                </tr>
                <tr class="building_subheader building_second_subheader">
                  <th class="floor_no">PIĘTRA</th>
                  <th class="total_space_3 total_space">(NLA)</th>
                  <th class="available_space_3">m<sup>2</sup></th>
                  <th class="space_description_3">OPIS</th>
                  <th class="available_from_3">OD KIEDY</th>
                  <th class="total_space_3 total_space">(NLA)</th>
                  <th class="available_space_3">m<sup>2</sup></th>
                  <th class="space_description_3">OPIS</th>
                  <th class="available_from_3">OD KIEDY</th>
                  <th class="total_space_3 total_space">(NLA)</th>
                  <th class="available_space_3">m<sup>2</sup></th>
                  <th class="space_description_3">OPIS</th>
                  <th class="available_from_3">OD KIEDY</th>
                </tr>
                <tr>
                  <td class="floor_no">6</td>
                  <td class="total_space_value space_body">2 285.6a</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_0_6" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                  <td class="combine_minus_value"></td>
                  <td></td>
                  <td class="space_body"></td>
                  <td></td>
                  <td></td>
                  <td class="combine_minus_value"></td>
                  <td></td>
                  <td class="space_body"></td>
                  <td></td>
                  <td></td>
                </tr>
                <tr>
                  <td class="floor_no">5</td>
                  <td class="total_space_value space_body">2 285.5a</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_0_5" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                  <td class="combine_minus_value"></td>
                  <td class="total_space_value space_body">0</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_1_5" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                  <td class="combine_minus_value"></td>
                  <td></td>
                  <td class="space_body"></td>
                  <td></td>
                  <td></td>
                </tr>
                <tr>
                  <td class="floor_no">4</td>
                  <td class="total_space_value space_body">2 285.4a</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_0_4" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                  <td class="combine_minus_value"></td>
                  <td class="total_space_value space_body">0</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_1_4" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                  <td class="combine_minus_value"></td>
                  <td></td>
                  <td class="space_body"></td>
                  <td></td>
                  <td></td>
                </tr>
                <tr>
                  <td class="floor_no">3</td>
                  <td class="total_space_value space_body">2 285.3a</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_0_3" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                  <td class="combine_minus_value"></td>
                  <td class="total_space_value space_body">0</td>
                  <td class="available_space_value available_space_body">305</td>
                  <td id="modules_count_0_1_3" class="space_description_value available_space_body">moduł B</td>
                  <td class="available_from_value available_space_body">od zaraz</td>
                  <td class="combine_minus_value"></td>
                  <td></td>
                  <td class="space_body"></td>
                  <td></td>
                  <td></td>
                </tr>
                <tr>
                  <td class="floor_no">2</td>
                  <td class="total_space_value space_body">2 285.2a</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_0_2" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                  <td class="combine_minus_value"></td>
                  <td class="total_space_value space_body">0</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_1_2" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                  <td class="combine_minus_value"></td>
                  <td></td>
                  <td class="space_body"></td>
                  <td></td>
                  <td></td>
                </tr>
                <tr>
                  <td class="floor_no">1</td>
                  <td class="total_space_value space_body">2 285.1a</td>
                  <td class="available_space_value available_space_body">551</td>
                  <td id="modules_count_0_0_1" class="space_description_value available_space_body">moduł B</td>
                  <td class="available_from_value available_space_body">od zaraz</td>
                  <td class="combine_minus_value"></td>
                  <td class="total_space_value space_body">0</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_1_1" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                  <td class="combine_minus_value"></td>
                  <td class="total_space_value space_body">0</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_2_1" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                </tr>
                <tr>
                  <td class="floor_no">0</td>
                  <td class="total_space_value space_body">2 285.0a</td>
                  <td class="available_space_value available_space_body">808</td>
                  <td id="modules_count_0_0_0" class="has_modules space_description_value available_space_body">6 modułów</td>
                  <td class="available_from_value available_space_body">od zaraz</td>
                  <td class="combine_minus_value"></td>
                  <td class="total_space_value space_body">0</td>
                  <td class="available_space_value available_space_body">371</td>
                  <td id="modules_count_0_1_0" class="has_modules space_description_value available_space_body">3 moduły</td>
                  <td class="available_from_value available_space_body">od zaraz</td>
                  <td class="combine_minus_value"></td>
                  <td class="total_space_value space_body">0</td>
                  <td class="available_space_value available_space_body">244</td>
                  <td id="modules_count_0_2_0" class="has_modules space_description_value available_space_body">moduł H</td>
                  <td class="available_from_value available_space_body">od zaraz</td>
                </tr>
                <tr id="floor_0_0_0" class="table_row_invisible">
                  <td class="empty_cell_floor_no module_data"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value">347</td>
                  <td class="module_data space_description_value">moduł H</td>
                  <td class="module_data available_from_value">od zaraz</td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value">186</td>
                  <td class="module_data space_description_value">moduł H</td>
                  <td class="module_data available_from_value">od zaraz</td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value"></td>
                  <td class="module_data space_description_value"></td>
                  <td class="module_data available_from_value"></td>
                </tr>
                <tr id="floor_0_0_1" class="table_row_invisible">
                  <td class="empty_cell_floor_no module_data"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value">55</td>
                  <td class="module_data space_description_value">moduł H</td>
                  <td class="module_data available_from_value">od zaraz</td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value">54</td>
                  <td class="module_data space_description_value">moduł H</td>
                  <td class="module_data available_from_value">od zaraz</td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value"></td>
                  <td class="module_data space_description_value"></td>
                  <td class="module_data available_from_value"></td>
                </tr>
                <tr id="floor_0_0_2" class="table_row_invisible">
                  <td class="empty_cell_floor_no module_data"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value">53</td>
                  <td class="module_data space_description_value">moduł H</td>
                  <td class="module_data available_from_value">od zaraz</td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value">131</td>
                  <td class="module_data space_description_value">moduł H</td>
                  <td class="module_data available_from_value">od zaraz</td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value"></td>
                  <td class="module_data space_description_value"></td>
                  <td class="module_data available_from_value"></td>
                </tr>
                <tr id="floor_0_0_3" class="table_row_invisible">
                  <td class="empty_cell_floor_no module_data"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value">43</td>
                  <td class="module_data space_description_value">moduł H</td>
                  <td class="module_data available_from_value">od zaraz</td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value"></td>
                  <td class="module_data space_description_value"></td>
                  <td class="module_data available_from_value"></td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value"></td>
                  <td class="module_data space_description_value"></td>
                  <td class="module_data available_from_value"></td>
                </tr>
                <tr id="floor_0_0_4" class="table_row_invisible">
                  <td class="empty_cell_floor_no module_data"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value">35</td>
                  <td class="module_data space_description_value">moduł H</td>
                  <td class="module_data available_from_value">od zaraz</td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value"></td>
                  <td class="module_data space_description_value"></td>
                  <td class="module_data available_from_value"></td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value"></td>
                  <td class="module_data space_description_value"></td>
                  <td class="module_data available_from_value"></td>
                </tr>
                <tr id="floor_0_0_5" class="table_row_invisible">
                  <td class="empty_cell_floor_no module_data"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value">275</td>
                  <td class="module_data space_description_value">moduł H</td>
                  <td class="module_data available_from_value">od zaraz</td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value"></td>
                  <td class="module_data space_description_value"></td>
                  <td class="module_data available_from_value"></td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value"></td>
                  <td class="module_data space_description_value"></td>
                  <td class="module_data available_from_value"></td>
                </tr>
                <tr>
                  <td class="building_footer_label">RAZEM</td>
                  <td class="building_footer_value">15 995</td>
                  <td class="building_footer_value">1 359</td>
                  <td class="building_footer_value" colspan="2"></td>
                  <td class="building_footer_value"></td>
                  <td class="building_footer_value">0</td>
                  <td class="building_footer_value">676</td>
                  <td class="building_footer_value" colspan="2"></td>
                  <td class="building_footer_value"></td>
                  <td class="building_footer_value">0</td>
                  <td class="building_footer_value">244</td>
                  <td class="building_footer_value" colspan="2"></td>
                </tr>
              </table>
              <table class="building_space_table" id="building_space_table_1">
                <tr class="building_header">
                  <th></th>
                  <th class="building_header_label" colspan="4">BUDYNEK 4</th>
                </tr>
                <tr class="building_subheader building_first_subheader">
                  <th class="floor_no"></th>
                  <th class="total_space">CAŁK. POW. m<sup>2</sup></th>
                  <th class="available_space_top_label" colspan="3">DOSTĘPNE POWIERZCHNIE</th>
                </tr>
                <tr class="building_subheader building_second_subheader">
                  <th class="floor_no">PIĘTRA</th>
                  <th class="total_space_3 total_space">(NLA)</th>
                  <th class="available_space_3">m<sup>2</sup></th>
                  <th class="space_description_3">OPIS</th>
                  <th class="available_from_3">OD KIEDY</th>
                </tr>
                <tr>
                  <td class="floor_no">1-3</td>
                  <td class="total_space_value space_body">2 141</td>
                  <td class="available_space_value available_space_body">2 141</td>
                  <td id="modules_count_1_0_1-3" class="space_description_value available_space_body">całe piętro B</td>
                  <td class="available_from_value available_space_body">od zaraz</td>
                </tr>
                <tr>
                  <td class="floor_no">0</td>
                  <td class="total_space_value space_body">1 624</td>
                  <td class="available_space_value available_space_body">1 624</td>
                  <td id="modules_count_1_0_0" class="space_description_value available_space_body">całe piętro B</td>
                  <td class="available_from_value available_space_body">od zaraz</td>
                </tr>
                <tr>
                  <td class="building_footer_label">RAZEM</td>
                  <td class="building_footer_value">8 047</td>
                  <td class="building_footer_value">8 047</td>
                  <td class="building_footer_value" colspan="2"></td>
                </tr>
              </table>
            </div>
            <div id="typical_floor_plan_header">
              Plan typowego piętra
            </div>
            <div id="typical_floor_plan_container">
              <div id="typical_floor_plan_inner_container">
                <img id="typical_floor_plan" src="/images/galeria/328/pietro-adgar_park_west.jpg" alt="Adgar Park West"/>
              </div>
            </div>
            <div id="disclaimer">
              Niniejsza broszurka ma charakter wyłącznie informacyjny i nie stanowi elementu wiążącej oferty lub kontraktu.
            </div>
          </div>
        </div>
      </div>
    </div>
    <div id="page_footer_container">
      <div id="footer">
        <div id="top_footer_container" class="footer_container">
          <div id="office_1">
            <a href="http://www.cushmanwakefield.pl/pl-pl/"><img alt="remobile" src="/images/layout/logo.png"></a>
          </div>
          <div id="office_2">
            <p>Nie masz czasu szukać? Zadzwoń lub napisz</p>
            <p class="telephone">+48 22 820 20 20</p>
            <p class="email">office@remobile.pl</p>
          </div>
          <div id="cw_pages">
            <a href="/pl/kontakt" class="front_link front_link_abstract" rel="nofollow">Biuro w Warszawie</a> <a href="/pl/kontakt" class="front_link front_link_abstract" rel="nofollow">Biuro w Krakowie</a> <a href="/pl/kontakt" class="front_link front_link_abstract" rel="nofollow">Biuro we Wrocławiu</a> <a href="/pl/kontakt" class="front_link front_link_abstract" rel="nofollow">Biuro w Gdańsku</a> <a href="/pl/kontakt" class="front_link front_link_abstract" rel="nofollow">Biuro w Katowicach</a> <a href="/pl/kontakt" class="front_link front_link_abstract" rel="nofollow">Biuro w Lodzi</a>
          </div>
        </div>
        <div id="bottom_footer_container" class="footer_container">
          <div id="footer_menu">
            <ul class="navigation">
              <li ><a href="/pl/regulamin" >Regulamin</a></li>
              <li ><a href="/pl/polityka-prywatnosci" >Polityka prywatności</a></li>
              <li ><a href="/pl/kontakt" >Kontakt</a></li>
            </ul>
          </div>
          <div id="copyrights">
            &copy; Cushman & Wakefield Polska Sp. z o.o. 2016. Wszelkie prawa zastrzeżone.
          </div>
        </div>
      </div>
    </div>
    """

z = """
    <table class="building_space_table" id="building_space_table_0">
                <tr class="building_header">
                  <th></th>
                  <th class="building_header_label" colspan="5">BUDYNEK A</th>
                  <th class="building_header_label" colspan="5">BUDYNEK B</th>
                  <th class="building_header_label" colspan="4">BUDYNEK C</th>
                </tr>
                <tr class="building_subheader building_first_subheader">
                  <th class="floor_no"></th>
                  <th class="total_space">CAŁK. POW. m<sup>2</sup></th>
                  <th class="available_space_top_label" colspan="3">DOSTĘPNE POWIERZCHNIE</th>
                  <th rowspan="2" class="combine"><span>ŁĄCZENIE</span></th>
                  <th class="total_space">CAŁK. POW. m<sup>2</sup></th>
                  <th class="available_space_top_label" colspan="3">DOSTĘPNE POWIERZCHNIE</th>
                  <th rowspan="2" class="combine"><span>ŁĄCZENIE</span></th>
                  <th class="total_space">CAŁK. POW. m<sup>2</sup></th>
                  <th class="available_space_top_label" colspan="3">DOSTĘPNE POWIERZCHNIE</th>
                </tr>
                <tr class="building_subheader building_second_subheader">
                  <th class="floor_no">PIĘTRA</th>
                  <th class="total_space_3 total_space">(NLA)</th>
                  <th class="available_space_3">m<sup>2</sup></th>
                  <th class="space_description_3">OPIS</th>
                  <th class="available_from_3">OD KIEDY</th>
                  <th class="total_space_3 total_space">(NLA)</th>
                  <th class="available_space_3">m<sup>2</sup></th>
                  <th class="space_description_3">OPIS</th>
                  <th class="available_from_3">OD KIEDY</th>
                  <th class="total_space_3 total_space">(NLA)</th>
                  <th class="available_space_3">m<sup>2</sup></th>
                  <th class="space_description_3">OPIS</th>
                  <th class="available_from_3">OD KIEDY</th>
                </tr>
                <tr>
                  <td class="floor_no">6</td>
                  <td class="total_space_value space_body">2 285.6</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_0_6" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                  <td class="combine_minus_value"></td>
                  <td></td>
                  <td class="space_body"></td>
                  <td></td>
                  <td></td>
                  <td class="combine_minus_value"></td>
                  <td></td>
                  <td class="space_body"></td>
                  <td></td>
                  <td></td>
                </tr>
                <tr>
                  <td class="floor_no">5</td>
                  <td class="total_space_value space_body">2 285.5</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_0_5" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                  <td class="combine_minus_value"></td>
                  <td class="total_space_value space_body">0</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_1_5" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                  <td class="combine_minus_value"></td>
                  <td></td>
                  <td class="space_body"></td>
                  <td></td>
                  <td></td>
                </tr>
                <tr>
                  <td class="floor_no">4</td>
                  <td class="total_space_value space_body">2 285.4</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_0_4" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                  <td class="combine_minus_value"></td>
                  <td class="total_space_value space_body">0</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_1_4" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                  <td class="combine_minus_value"></td>
                  <td></td>
                  <td class="space_body"></td>
                  <td></td>
                  <td></td>
                </tr>
                <tr>
                  <td class="floor_no">3</td>
                  <td class="total_space_value space_body">2 285.3</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_0_3" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                  <td class="combine_minus_value"></td>
                  <td class="total_space_value space_body">0</td>
                  <td class="available_space_value available_space_body">305</td>
                  <td id="modules_count_0_1_3" class="space_description_value available_space_body">moduł B</td>
                  <td class="available_from_value available_space_body">od zaraz</td>
                  <td class="combine_minus_value"></td>
                  <td></td>
                  <td class="space_body"></td>
                  <td></td>
                  <td></td>
                </tr>
                <tr>
                  <td class="floor_no">2</td>
                  <td class="total_space_value space_body">2 285.2</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_0_2" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                  <td class="combine_minus_value"></td>
                  <td class="total_space_value space_body">0</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_1_2" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                  <td class="combine_minus_value"></td>
                  <td></td>
                  <td class="space_body"></td>
                  <td></td>
                  <td></td>
                </tr>
                <tr>
                  <td class="floor_no">1</td>
                  <td class="total_space_value space_body">2 285.1</td>
                  <td class="available_space_value available_space_body">551</td>
                  <td id="modules_count_0_0_1" class="space_description_value available_space_body">moduł B</td>
                  <td class="available_from_value available_space_body">od zaraz</td>
                  <td class="combine_minus_value"></td>
                  <td class="total_space_value space_body">0</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_1_1" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                  <td class="combine_minus_value"></td>
                  <td class="total_space_value space_body">0</td>
                  <td class="available_space_value space_body">0</td>
                  <td id="modules_count_0_2_1" class="space_description_value space_body">wynajęte</td>
                  <td class="available_from_value space_body">n/a</td>
                </tr>
                <tr>
                  <td class="floor_no">0</td>
                  <td class="total_space_value space_body">2 285.0</td>
                  <td class="available_space_value available_space_body">808</td>
                  <td id="modules_count_0_0_0" class="has_modules space_description_value available_space_body">6 modułów</td>
                  <td class="available_from_value available_space_body">od zaraz</td>
                  <td class="combine_minus_value"></td>
                  <td class="total_space_value space_body">0</td>
                  <td class="available_space_value available_space_body">371</td>
                  <td id="modules_count_0_1_0" class="has_modules space_description_value available_space_body">3 moduły</td>
                  <td class="available_from_value available_space_body">od zaraz</td>
                  <td class="combine_minus_value"></td>
                  <td class="total_space_value space_body">0</td>
                  <td class="available_space_value available_space_body">244</td>
                  <td id="modules_count_0_2_0" class="has_modules space_description_value available_space_body">moduł H</td>
                  <td class="available_from_value available_space_body">od zaraz</td>
                </tr>
                <tr id="floor_0_0_0" class="table_row_invisible">
                  <td class="empty_cell_floor_no module_data"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value">347</td>
                  <td class="module_data space_description_value">moduł H</td>
                  <td class="module_data available_from_value">od zaraz</td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value">186</td>
                  <td class="module_data space_description_value">moduł H</td>
                  <td class="module_data available_from_value">od zaraz</td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value"></td>
                  <td class="module_data space_description_value"></td>
                  <td class="module_data available_from_value"></td>
                </tr>
                <tr id="floor_0_0_1" class="table_row_invisible">
                  <td class="empty_cell_floor_no module_data"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value">55</td>
                  <td class="module_data space_description_value">moduł H</td>
                  <td class="module_data available_from_value">od zaraz</td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value">54</td>
                  <td class="module_data space_description_value">moduł H</td>
                  <td class="module_data available_from_value">od zaraz</td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value"></td>
                  <td class="module_data space_description_value"></td>
                  <td class="module_data available_from_value"></td>
                </tr>
                <tr id="floor_0_0_2" class="table_row_invisible">
                  <td class="empty_cell_floor_no module_data"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value">53</td>
                  <td class="module_data space_description_value">moduł H</td>
                  <td class="module_data available_from_value">od zaraz</td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value">131</td>
                  <td class="module_data space_description_value">moduł H</td>
                  <td class="module_data available_from_value">od zaraz</td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value"></td>
                  <td class="module_data space_description_value"></td>
                  <td class="module_data available_from_value"></td>
                </tr>
                <tr id="floor_0_0_3" class="table_row_invisible">
                  <td class="empty_cell_floor_no module_data"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value">43</td>
                  <td class="module_data space_description_value">moduł H</td>
                  <td class="module_data available_from_value">od zaraz</td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value"></td>
                  <td class="module_data space_description_value"></td>
                  <td class="module_data available_from_value"></td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value"></td>
                  <td class="module_data space_description_value"></td>
                  <td class="module_data available_from_value"></td>
                </tr>
                <tr id="floor_0_0_4" class="table_row_invisible">
                  <td class="empty_cell_floor_no module_data"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value">35</td>
                  <td class="module_data space_description_value">moduł H</td>
                  <td class="module_data available_from_value">od zaraz</td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value"></td>
                  <td class="module_data space_description_value"></td>
                  <td class="module_data available_from_value"></td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value"></td>
                  <td class="module_data space_description_value"></td>
                  <td class="module_data available_from_value"></td>
                </tr>
                <tr id="floor_0_0_5" class="table_row_invisible">
                  <td class="empty_cell_floor_no module_data"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value">275</td>
                  <td class="module_data space_description_value">moduł H</td>
                  <td class="module_data available_from_value">od zaraz</td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value"></td>
                  <td class="module_data space_description_value"></td>
                  <td class="module_data available_from_value"></td>
                  <td class="module_data module_combine"></td>
                  <td class="module_data empty_cell_total_space"></td>
                  <td class="module_data available_space_value"></td>
                  <td class="module_data space_description_value"></td>
                  <td class="module_data available_from_value"></td>
                </tr>
                <tr>
                  <td class="building_footer_label">RAZEM</td>
                  <td class="building_footer_value">15 995</td>
                  <td class="building_footer_value">1 359</td>
                  <td class="building_footer_value" colspan="2"></td>
                  <td class="building_footer_value"></td>
                  <td class="building_footer_value">0</td>
                  <td class="building_footer_value">676</td>
                  <td class="building_footer_value" colspan="2"></td>
                  <td class="building_footer_value"></td>
                  <td class="building_footer_value">0</td>
                  <td class="building_footer_value">244</td>
                  <td class="building_footer_value" colspan="2"></td>
                </tr>
              </table>
"""

def read_line(filename):
    #takes a file with urls
    #returns a list of urls
    file_path = path.relpath("miasta_b_urls/" + filename + ".txt")
    with open(file_path) as f:
        lines = f.read()
        return lines.split("\n")

def try_fetch(func):
    try:
        func
    except:
        pass

def fetch_html(src_url):
    #function takes url and returns pure html
    print(sw + "fetching html from " + src_url + sw)
    r = urllib2.urlopen(src_url)
    html = r.read()
    return html

def r_rest(html,extr):
    #find the extraction spot and return rest of string
    stop_no = html.find(extr) + 1
    rest_html = html[stop_no:]
    return rest_html

def nesting_dict(name, dict):
    #osadza budynkowy dict w słowniku ogólnym
    b_data[name] = dict

def finding_name(html, dict):
    #znajduje nazwę budynku i wstawia go w pole "name"
    rest_html = r_rest(r_rest(html, "<h1>"), ">")
    ex_stop_no = rest_html.find('<')
    dict["name"] = rest_html[0: ex_stop_no]

def finding_description(html, dict):
    #znajduje opis i wstawia go w pole "description'
    rest_html = r_rest(r_rest(html, '<div id="description"'), "\n")
    ex_stop_no = rest_html.find('<')
    dict["description"] = rest_html[20: ex_stop_no]

def finding_location(html, dict):
    #znajduje informacje o lokalizacji i zapisuje je dict["location"]
    dict["location"] = {}
    rest_html = r_rest(r_rest(r_rest(r_rest(html, '<td class="location_column'), ">"), '<div'), "\n")
    ex_stop_no = rest_html.find('\n')
    temp_location = rest_html[0: ex_stop_no]
    if "," in temp_location:
        stop = temp_location.find(",")
        #print stop
        dict["location"]["city"] = temp_location[0: stop].replace(" ", "")
        stop = stop + 2
        dict["location"]["district"] = temp_location[stop:]
    else:
        dict["location"]["city"] = temp_location[0:].replace(" ", "")
        dict["location"]["district"] = ""
    rest_html = r_rest(r_rest(rest_html, '<div'), "\n")
    ex_stop_no = rest_html.find('\n')
    dict["location"]["address"] = rest_html[24:ex_stop_no]

def finding_terms(html, dict):
    #znajduje informacje o warunkach najmu i zapisuje jest do dict["terms"]
    dict["terms"] = {}
    rest_html = r_rest(html, "Wyjściowe warunki najmu")
    rest_html = r_rest(r_rest(r_rest(rest_html, "Czynsz"),'class="table_field_value'),">")
    ex_stop_no = rest_html.find('<')
    dict["terms"]["rent"] = rest_html[0: ex_stop_no]
    rest_html = r_rest(r_rest(r_rest(rest_html, "pow. handlow"), 'class="table_field_value'), ">")
    ex_stop_no = rest_html.find('<')
    dict["terms"]["retail rent"] = rest_html[0: ex_stop_no]
    rest_html = r_rest(r_rest(r_rest(rest_html, "Koszty eksploatacyjne</"), 'class="table_field_value'), ">")
    ex_stop_no = rest_html.find('<')
    dict["terms"]["service charge"] = rest_html[0: ex_stop_no]
    rest_html = r_rest(r_rest(r_rest(rest_html, "parkingu naziemnego</"), 'class="table_field_value'), ">")
    ex_stop_no = rest_html.find('<')
    dict["terms"]["parking onground"] = rest_html[0: ex_stop_no]
    rest_html = r_rest(r_rest(r_rest(rest_html, "parkingu podziemnego</"), 'class="table_field_value'), ">")
    ex_stop_no = rest_html.find('<')
    dict["terms"]["parking underground"] = rest_html[0: ex_stop_no]
    rest_html = r_rest(r_rest(r_rest(rest_html, "Współczynnik miejsc parkingowych</"), 'class="table_field_value'), ">")
    ex_stop_no = rest_html.find('<')
    dict["terms"]["parking ratio"] = rest_html[0: ex_stop_no]

def finding_status(html, dict):
    #znajduje informacje o statusie budynku i zapisuje je do dict["building info"]
    dict["building info"] = {}
    rest_html = r_rest(html, "Informacje o budynku")
    rest_html = r_rest(r_rest(r_rest(rest_html, "Status budynku</"), 'class="table_field_value'), ">")
    ex_stop_no = rest_html.find('<')
    dict["building info"]["status"] = rest_html[0: ex_stop_no]
    rest_html = r_rest(r_rest(r_rest(rest_html, "wita pow. biurowa netto</"), 'class="table_field_value'), ">")
    ex_stop_no = rest_html.find('<')
    dict["building info"]["total space"] = rest_html[0: ex_stop_no]
    rest_html = r_rest(r_rest(r_rest(rest_html, "Data zakończenia budowy</"), 'class="table_field_value'), ">")
    ex_stop_no = rest_html.find('<')
    dict["building info"]["completion date"] = rest_html[0: ex_stop_no]
    rest_html = r_rest(r_rest(r_rest(rest_html, "pięter naziemnych</"), 'class="table_field_value'), ">")
    ex_stop_no = rest_html.find('<')
    dict["building info"]["no of onground floors"] = rest_html[0: ex_stop_no]
    rest_html = r_rest(r_rest(r_rest(rest_html, "pięter podziemnych</"), 'class="table_field_value'), ">")
    ex_stop_no = rest_html.find('<')
    dict["building info"]["no of underground floors"] = rest_html[0: ex_stop_no]
    rest_html = r_rest(r_rest(r_rest(rest_html, "Powierzchnia typowego piętra</"), 'class="table_field_value'), ">")
    ex_stop_no = rest_html.find('<')
    dict["building info"]["floor plate"] = rest_html[0: ex_stop_no]
    rest_html = r_rest(r_rest(r_rest(rest_html, "miejsc parkingowych naziemnych</"), 'class="table_field_value'), ">")
    ex_stop_no = rest_html.find('<')
    dict["building info"]["no of parking places onground"] = rest_html[0: ex_stop_no]
    rest_html = r_rest(r_rest(r_rest(rest_html, "miejsc parkingowych podziemnych</"), 'class="table_field_value'), ">")
    ex_stop_no = rest_html.find('<')
    dict["building info"]["no of parking places underground"] = rest_html[0: ex_stop_no]
    rest_html = r_rest(r_rest(r_rest(rest_html, "Minimalny okres najmu</"), 'class="table_field_value'), ">")
    ex_stop_no = rest_html.find('<')
    dict["building info"]["min lease term"] = rest_html[0: ex_stop_no]
    rest_html = r_rest(r_rest(r_rest(rest_html, "Współczynnik pow. wspólnych</"), 'class="table_field_value'), ">")
    ex_stop_no = rest_html.find('<')
    dict["building info"]["add-on factor"] = rest_html[0: ex_stop_no]

def stardard_status_test(s):
    #sprawdza czy elements standardu jest czy go nie ma
    if "inactive_table_field" in s:
        return 0
    else:
        return 1

def finding_standard(html, dict):
    #wyciąga elementy standardu, sprawdza czy są czy ich nie ma i zapisuje je do dict["building standard"]
    dict["building standard"] = {}
    rest_html = r_rest(html, "Standard wykończeń</")
    table_of_standard = rest_html[0:rest_html.find("</tbody>")]
    n = 0
    while n < 16:
        rest_html = r_rest(rest_html, 'table_field_label')
        ex_stop_no = rest_html.find('</td')
        temp_location = rest_html[0: ex_stop_no]
        temp_location2 = r_rest(r_rest(temp_location, "span"), ">")
        field_name = temp_location2[0:temp_location2.find("<")]
        dict["building standard"][field_name] = stardard_status_test(temp_location)
        n += 1


#=== finding av spaces ===

def finding_offices(html,dict):
    dict["rentable area"] = {}
    unclear_tables = []
    rest_html = html
    for e in range(phrase_count(rest_html, '<table class="building_space_table')):
        unclear_tables.append(preparing_table(rest_html))
        rest_html = r_rest(r_rest(r_rest(rest_html, '<table class="building_space_table'), '</table>'), ">")
    clear_tables = []
    #for e in unclear_tables:
    #    print e
    for e in unclear_tables:
        if checking_multibuildings(e) == True:
            clear_tables.append(e)
        else:
            d_table = deconstructing_table(e)
            #print d_table
            for table in range(phrase_count(d_table, '<table class="building_space_table')):
                clear_tables.append(d_table[0:(d_table.find(">", d_table.find('</table>'))) + 1])
                d_table = r_rest(r_rest(r_rest(d_table, '<table class="building_space_table'), '</table>'), ">")
    no = 1
    for e in clear_tables:
        #print "element " + str(no)
        #print e
        fetching_offices(e, dict["rentable area"], no)
        no += 1



fl_pattern = ['td class="total_space', \
              'td class="available_space', \
              'space_description', \
              'class="available_from']

fl_pattern_dict = {'td class="total_space' : "nla", \
              'td class="available_space' : "total av space", \
              'space_description' : "av space descr", \
              'class="available_from' : "since when"}

def fetching_offices(html, dict, no):
    #nazwa budynku
    b_no = "b no " + str(no)
    dict[b_no] = {}
    dict[b_no]["b name"] = extract_value(html, '<th class="building_header_label')
    #wynajmowalna powierzchnia
    dict[b_no]["b rentable area"] = {}
    #print phrase_count(html, 'class="floor_no')
    for e in range(phrase_count(html, 'class="floor_no')):
        floor_no = "floor " + str(extract_value(html, 'class="floor_no'))
        dict[b_no]["b rentable area"][floor_no] = {}
        fetching_floor(html, dict[b_no]["b rentable area"][floor_no])
        html = r_rest(html, '</tr>')

def fetching_floor(html, dict):
    #n = 1
    for e in fl_pattern:
        dict[fl_pattern_dict[e]] = extract_value(html, e)
        #n += 1

def extract_value(html, extr):
    beg = html.find(">", html.find(extr))
    beg = beg + 1
    value = html[beg:html.find("<", beg)]
    return value

#=== restructuring table === (not done)

def checking_multibuildings(html):
    if phrase_count(html, 'class="building_header_label"') == 1:
        return True
    else:
        return False

def phrase_count(html, x):
    n = 0
    r = 1
    while r > 0:
        r = html.find(x)
        r += 1
        html = html[r:]
        if r <= 0:
            break
        n += 1
    return n

def sep_check(html):
    #sprawdza czy w danym wierszu są
    nla_pos = html.find('class="total_space_value space_body">')
    sep_pos = html.find("$")
    #print nla_pos, sep_pos
    if nla_pos < sep_pos:
        return True
    if nla_pos > sep_pos:
        return False

#=== preparing table === (done)

def preparing_table(html):
    pure_table = extracting_table(html)
    table_parts = []
    header = getting_headers(pure_table)
    table_parts.append(header)
    for n in range(phrase_count(pure_table, '<td class="floor_no')):
        floor = getting_floors(pure_table)
        table_parts.append(floor)
        pure_table = r_rest(r_rest(pure_table, '<td class="floor_no'), "</tr")
    return "\n".join(table_parts)

def getting_headers(html):
    header_start = html.find('<th class="building_header')
    header_stop = html.find('</tr', header_start)
    header = html[header_start:header_stop]
    return header

def getting_floors(html):
    floor_start = html.find('<td class="floor_no')
    floor_stop = html.find('</tr', floor_start)
    floor = html[floor_start:floor_stop + 5]
    return floor

def extracting_table(html):
    #wyciąga html z samą tabelą
    table_start = html.find('<table class="building_space_table"')
    rest_html = html[table_start:html.find("</table>", table_start)]
    return rest_html

#=== decondstructing and reconstructing ===

def setting_separators(html):
    html = html.replace('<td class="combine_minus_value"></td>', "$")
    html = html.replace('</tr>', "$</tr>")
    html = html + "$"
    return html

def deconstructing_table(html):
    pure_table = setting_separators(html)
    pure_table_head = pure_table
    #print pure_table
    head_tables = []
    for n in range(phrase_count(html, '<th class="building_header')):
        #head_table = []
        header = dec_header(pure_table_head)
        head_tables.append(header)
        #head_tables.append(head_table)
        pure_table_head = r_rest(r_rest(pure_table_head, '<th class="building_header'), "</th")
    floor_table = []
    pure_table_floors = pure_table
    for n in range(phrase_count(html, '<td class="floor_no')):
        floor = dec_floor(pure_table_floors)
        floor_table.append(floor)
        pure_table_floors = r_rest(r_rest(pure_table_floors, '<td class="floor_no'), "</tr")
    spaces_tables = []
    pure_table_spaces = pure_table.replace('<td class="floor_no', "")
    #print pure_table_spaces
    while pure_table_spaces.find('<td') > 0:
        #if pure_table_spaces.find('<td class="floor_no') < pure_table_spaces.find('<td', pure_table_spaces.find('class="floor_no')):
            #pure_table_spaces = r_rest(r_rest(r_rest(pure_table_spaces, '<td class="floor_no'), "</td"), ">")
        space = dec_spaces(pure_table_spaces)
        spaces_tables.append(space)
        pure_table_spaces = r_rest(pure_table_spaces, "$")
        #print pure_table_spaces
    #print head_tables
    #print floor_table
    #print len(spaces_tables)
    #for e in spaces_tables:
        #print "element"
        #print e
    return reconstructing_table(head_tables, floor_table, spaces_tables)

def reconstructing_table(list1, list2, list3):
    all_tables = []
    for e in list1:
        temp_table = []
        temp_table.append('<table class="building_space_table">\n')
        all_tables.append(temp_table)
    n = 0
    for e in all_tables:
        e.append(list1[n])
        n += 1
    n = 0
    for e in list2:
        for list in all_tables:
            if '<td class="total_space_value space_body' in list3[n]:
                list.append(e)
                list.append(list3[n])
                list.append('</tr>')
            else:
                pass
            n += 1
    for e in all_tables:
        e.append('</table>')
    new_tables = []
    for e in all_tables:
        for s in e:
            new_tables.append(s)
    #for e in new_tables:
    #    print e
    new_table = "\n".join(new_tables)
    #print new_table
    return new_table
    """
    stara wersja
    for e in all_tables:
        e = "\n".join(e)
        e = str(e)
        new_tables.append(e)
    new_table = "\n".join(new_tables)
    new_table = new_table.replace("$", "")
    return new_table
    """

def dec_header(html):
    header_start = html.find('<th class="building_header')
    header_stop = html.find('</th', header_start)
    header = html[header_start:header_stop + 5]
    #stop_point = header_stop + 5
    return header

def dec_floor(html):
    floor_start = html.find('<td class="floor_no')
    floor_stop = html.find('</td', floor_start)
    floor = html[floor_start:floor_stop + 5]
    #stop_point = floor_stop + 5
    return floor

def dec_spaces(html):
    floor_start = html.find('<td')
    floor_stop = html.find('$', floor_start)
    floor = html[floor_start:floor_stop + 1]
    #stop_point = floor_stop + 5
    return floor

"""
data = {}
#z = deconstructing_table(y)
#print z
finding_offices(y, data)
print data

"""

urls = read_line("test")

for e in urls:
    try:
        html = fetch_html(e)
        html = r_rest(html, '<div id="offer_container">')
        data = {}
        finding_name(html, data)
        finding_description(html, data)
        finding_location(html, data)
        finding_terms(html, data)
        finding_status(html, data)
        finding_standard(html, data)
        finding_offices(html, data)
        nesting_dict(data["name"], data)
    except Exception as err:
        print "An error occurred: " + str(err)
        print "Could not fetch: " + str(e)
        error_urls.append(e)
        pass


#print b_data

with open('result.json', 'w') as fp:
    json.dump(b_data, fp, sort_keys=True, indent=2)

for url in error_urls:
    with open('errors.txt', 'w') as ef:
        ef.write("%s\n" % url)

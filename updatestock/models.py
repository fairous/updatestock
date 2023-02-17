from django.db import models


brand_name_choice = (
    ('HONDA', 'HONDA'),
    ('YAMAHA', 'YAMAHA'),
    ('BAJAJ', 'BAJAJ'),
    ('TVS', 'TVS'),
    ('HERO', 'HERO'),
    ('SUZUKI', 'SUZUKI'),
)

class Brand(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

bike_name_choice = (
    ('DIO', 'DIO'),
    ('GRAZIA', 'GRAZIA'),
    ('RAY-ZR', 'RAY-ZR'),
    ('FZ', 'FZ'),
    ('BURGMAN', 'BURGMAN'),
    ('WEGO', 'WEGO'),
    ('PEP', 'PEP'),
    ('N-TOQ', 'N-TOQ'),
    ('PLEASURE', 'PLEASURE'),
    ('DISC-135', 'DISC-135'),
    ('DISC-125', 'DISC-125'),
    ('DISC-150', 'DISC-150'),
    ('CT-100', 'CT-100'),
    ('PULS-135','PULS-135'),
    ('PULS-150','PULS-150'),
    ('NS-200','NS-200'),
)

class Bike(models.Model):
    name = models.ForeignKey(Brand, on_delete=models.CASCADE)
    bike_name = models.CharField(max_length=50, blank=True, null=True, choices=bike_name_choice)

    def __str__(self):
        return self.bike_name


class Stock(models.Model):
    brand_name = models.ForeignKey(Brand, on_delete=models.CASCADE)
    bike_name = models.ForeignKey(Bike, on_delete=models.CASCADE, blank=True, null=True)
    part_number = models.CharField(max_length=50, blank=True, null=True)
    part_name = models.CharField(max_length=50, blank=True, null=True)
    mrp_amount = models.CharField(max_length=50, blank=True, null=True)
    exchange_rate = models.CharField(max_length=50, blank=True, null=True)
    shipping_amount = models.CharField(max_length=50, blank=True, null=True)
    cost = models.CharField(max_length=50, blank=True, null=True)
    margine = models.CharField(max_length=50, blank=True, null=True)
    add = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    receive_quantity = models.IntegerField(default=0, blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default=0, blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default=0, blank=True, null=True)
    export_to_CSV = models.BooleanField(default=False)
    last_updated = models.DateField(auto_now_add=False, auto_now=True)
    timestamp = models.DateField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f"{self.brand_name} {self.bike_name} {self.part_number} {self.part_name}"



class StockHistory(models.Model):
    brand_name = models.ForeignKey(Brand, on_delete=models.CASCADE)
    bike_name = models.ForeignKey(Bike, on_delete=models.CASCADE, blank=True, null=True)
    part_number = models.CharField(max_length=50, blank=True, null=True)
    part_name = models.CharField(max_length=50, blank=True, null=True)
    mrp_amount = models.CharField(max_length=50, blank=True, null=True)
    exchange_rate = models.CharField(max_length=50, blank=True, null=True)
    shipping_amount = models.CharField(max_length=50, blank=True, null=True)
    cost = models.CharField(max_length=50, blank=True, null=True)
    margine = models.CharField(max_length=50, blank=True, null=True)
    add = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    receive_quantity = models.IntegerField(default=0, blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default=0, blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default=0, blank=True, null=True)
    export_to_CSV = models.BooleanField(default=False)
    last_updated = models.DateField(auto_now_add=False, auto_now=True)
    timestamp = models.DateField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f"{self.brand_name} {self.bike_name} {self.part_number} {self.part_name}"



class Invoice(models.Model):
    invoice_number = models.IntegerField(blank=True, null=True)
    invoice_date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    name = models.CharField('Customer Name', max_length=120, default='', blank=True, null=True)

    line_one_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_one_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_one_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_one_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_one_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_one_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_two_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_two_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_two_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_two_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_two_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_two_total_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)

    line_three_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_three_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_three_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_three_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_three_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_three_total_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)

    line_four_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_four_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_four_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_four_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_four_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_four_total_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)

    line_five_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_five_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_five_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_five_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_five_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_five_total_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)

    line_six_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_six_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_six_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_six_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_six_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_six_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_seven_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_seven_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_seven_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_seven_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_seven_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_seven_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_eight_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_eight_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_eight_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_eight_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_eight_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_eight_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_nine_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True)
    line_nine_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_nine_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_nine_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_nine_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_nine_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_ten_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_ten_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_ten_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_ten_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_ten_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_ten_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)


    line_eleven_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_eleven_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_eleven_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_eleven_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_eleven_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_eleven_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_twelve_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_twelve_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_twelve_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_twelve_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_twelve_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_twelve_total_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)

    line_thirteen_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_thirteen_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_thirteen_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_thirteen_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_thirteen_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_thirteen_total_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)

    line_fourteen_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_fourteen_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_fourteen_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_fourteen_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_fourteen_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_fourteen_total_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)

    line_fifteen_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_fifteen_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_fifteen_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_fifteen_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_fifteen_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_fifteen_total_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)

    line_sixteen_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_sixteen_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_sixteen_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_sixteen_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_sixteen_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_sixteen_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_seventeen_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_seventeen_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_seventeen_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_seventeen_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_seventeen_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_seventeen_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_eighteen_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_eighteen_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_eighteen_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_eighteen_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_eighteen_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_eighteen_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_nineteen_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_nineteen_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_nineteen_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_nineteen_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_nineteen_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_nineteen_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_twenty_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_twenty_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_twenty_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_twenty_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_twenty_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_twenty_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_twentyone_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_twentyone_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_twentyone_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_twentyone_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_twentyone_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_twentyone_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_twentytwo_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_twentytwo_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_twentytwo_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_twentytwo_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_twentytwo_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_twentytwo_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_twentythree_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_twentythree_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_twentythree_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_twentythree_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_twentythree_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_twentythree_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_twentyfour_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_twentyfour_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_twentyfour_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_twentyfour_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_twentyfour_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_twentyfour_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_twentyfive_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_twentyfive_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_twentyfive_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_twentyfive_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_twentyfive_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_twentyfive_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_twentysix_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_twentysix_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_twentysix_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_twentysix_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_twentysix_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_twentysix_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_twentyseven_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_twentyseven_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_twentyseven_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_twentyseven_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_twentyseven_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_twentyseven_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_twentyeight_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_twentyeight_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_twentyeight_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_twentyeight_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_twentyeight_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_twentyeight_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_twentynine_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_twentynine_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_twentynine_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_twentynine_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_twentynine_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_twentynine_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    line_thirty_bike_name = models.CharField('Bike Name', max_length=120, default='', blank=True, null=True, choices=bike_name_choice)
    line_thirty_part_number = models.CharField('Part Number', max_length=120, default='', blank=True, null=True)
    line_thirty_part_name = models.CharField('Part Name', max_length=120, default='', blank=True, null=True)
    line_thirty_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_thirty_unit_price = models.IntegerField('Unit Price Rs', default=0, blank=True, null=True)
    line_thirty_total_price = models.IntegerField('Line Total Rs', default=0, blank=True, null=True)

    phone_number = models.CharField(max_length=120, default='', blank=True, null=True)
    total = models.IntegerField('Total Rs', default='0', blank=True, null=True)
    balance = models.IntegerField(default='0', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True)
    paid = models.BooleanField(default=False)
    invoice_type_choice = (
        ('Receipt', 'Receipt'),
        ('Proforma Invoice', 'Proforma Invoice'),
        ('Invoice', 'Invoice'),
    )
    invoice_type = models.CharField(max_length=50, default='', blank=True, null=True, choices=invoice_type_choice)
    comments = models.TextField(max_length=3000, default='', blank=True, null=True)

    def __unicode__(self):
        return self.name + '  ' + str(self.invoice_number)


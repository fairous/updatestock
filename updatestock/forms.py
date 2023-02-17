# from django import forms
# from . models import Stock
#
#
# class StockCreateForms(forms.ModelForm):
#     class Meta:
#         model = Stock
#         fields = ['brand_name', 'bike_name', 'part_number', 'part_name', 'mrp_amount',
#                   'exchange_rate', 'shipping_amount', 'cost', 'margine', 'add', 'quantity',
#                   'receive_quantity', 'receive_by', 'issue_quantity', 'issue_by', 'issue_to',
#                   'created_by', 'reorder_level', 'export_to_CSV' ]


from django import forms
from .models import *


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['brand_name', 'bike_name', 'part_number', 'part_name', 'quantity', 'mrp_amount',
                  'exchange_rate', 'cost', 'margine', 'add', 'shipping_amount', 'created_by']

    def clean_bike_name(self):
        bike_name = self.cleaned_data.get('bike_name')
        if not bike_name:
            raise forms.ValidationError('This field is required')
        return bike_name

    def clean_part_number(self):
        part_number = self.cleaned_data.get('part_number')
        if not part_number:
            raise forms.ValidationError('This field is required')

        for instance in Stock.objects.all():
            if instance.part_number == part_number:
                raise forms.ValidationError(str(part_number) + ' is already created')
        return part_number

    def clean_part_name(self):
        part_name = self.cleaned_data.get('part_name')
        if not part_name:
            raise forms.ValidationError('This field is required')
        return part_name


class StockHistorySearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    class Meta:
        model = StockHistory
        fields = ['bike_name', 'part_name', 'start_date', 'end_date']


class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)

    class Meta:
        model = Stock
        fields = ['bike_name', 'part_number', 'part_name']


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['brand_name', 'bike_name', 'part_number', 'part_name', 'quantity',
                  'mrp_amount', 'exchange_rate', 'cost', 'margine', 'add', 'shipping_amount', 'created_by']


class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['issue_quantity', 'issue_by']


class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['receive_quantity', 'receive_by']


class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']


from django.contrib import admin
from django import forms
from .models import Invoice

required = 'This field is required'


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = fields = '__all__'

    def clean_invoice_number(self):
        invoice_number = self.cleaned_data.get('invoice_number')
        if not invoice_number:
            raise forms.ValidationError(required)
        return invoice_number
        fields = fields = '__all__'
        exclude = ()
        fields = ['name', 'phone_number', 'invoice_date', 'invoice_number',
                  'line_one_bike_name', 'line_one_part_number', 'line_one_part_name', 'line_one_quantity',
                  'line_one_unit_price', 'line_one_total_price',
                  'line_two_bike_name', 'line_two_part_number', 'line_two_part_name', 'line_two_quantity',
                  'line_two_unit_price', 'line_two_total_price',
                  'line_three_bike_name', 'line_three_part_number', 'line_three_part_name',
                  'line_three_quantity',
                  'line_three_unit_price', 'line_three_total_price',
                  'line_four_bike_name', 'line_four_part_number', 'line_four_part_name', 'line_four_quantity',
                  'line_four_unit_price', 'line_four_total_price',
                  'line_five_bike_name', 'line_five_part_number', 'line_five_part_name', 'line_five_quantity',
                  'line_five_unit_price', 'line_five_total_price',

                  'line_six_bike_name', 'line_six_part_number', 'line_six_part_name', 'line_six_quantity',
                  'line_six_unit_price', 'line_six_total_price',
                  'line_seven_bike_name', 'line_seven_part_number', 'line_seven_part_name',
                  'line_seven_quantity',
                  'line_seven_unit_price', 'line_seven_total_price',
                  'line_eight_bike_name', 'line_eight_part_number', 'line_eight_part_name',
                  'line_eight_quantity',
                  'line_eight_unit_price', 'line_eight_total_price',
                  'line_nine_bike_name', 'line_nine_part_number', 'line_nine_part_name', 'line_nine_quantity',
                  'line_nine_unit_price', 'line_nine_total_price',
                  'line_ten_bike_name', 'line_ten_part_number', 'line_ten_part_name', 'line_ten_quantity',
                  'line_ten_unit_price', 'line_ten_total_price', 'line_one_bike_name', 'line_one_part_number',
                  'line_one_part_name', 'line_one_quantity',
                  'line_one_unit_price', 'line_one_total_price',
                  'line_two_bike_name', 'line_two_part_number', 'line_two_part_name', 'line_two_quantity',
                  'line_two_unit_price', 'line_two_total_price',
                  'line_three_bike_name', 'line_three_part_number', 'line_three_part_name',
                  'line_three_quantity',
                  'line_three_unit_price', 'line_three_total_price',
                  'line_four_bike_name', 'line_four_part_number', 'line_four_part_name', 'line_four_quantity',
                  'line_four_unit_price', 'line_four_total_price',
                  'line_five_bike_name', 'line_five_part_number', 'line_five_part_name', 'line_five_quantity',
                  'line_five_unit_price', 'line_five_total_price',

                  'line_six_bike_name', 'line_six_part_number', 'line_six_part_name', 'line_six_quantity',
                  'line_six_unit_price', 'line_six_total_price',
                  'line_seven_bike_name', 'line_seven_part_number', 'line_seven_part_name',
                  'line_seven_quantity',
                  'line_seven_unit_price', 'line_seven_total_price',
                  'line_eight_bike_name', 'line_eight_part_number', 'line_eight_part_name',
                  'line_eight_quantity',
                  'line_eight_unit_price', 'line_eight_total_price',
                  'line_nine_bike_name', 'line_nine_part_number', 'line_nine_part_name', 'line_nine_quantity',
                  'line_nine_unit_price', 'line_nine_total_price',
                  'line_ten_bike_name', 'line_ten_part_number', 'line_ten_part_name', 'line_ten_quantity',
                  'line_ten_unit_price', 'line_ten_total_price',

                  'line_eleven_bike_name', 'line_eleven_part_number', 'line_eleven_part_name',
                  'line_eleven_quantity',
                  'line_eleven_unit_price', 'line_eleven_total_price',
                  'line_twelve_bike_name', 'line_twelve_part_number', 'line_twelve_part_name',
                  'line_twelve_quantity',
                  'line_twelve_unit_price', 'line_twelve_total_price',
                  'line_thirteen_bike_name', 'line_thirteen_part_number', 'line_thirteen_part_name',
                  'line_thirteen_quantity',
                  'line_thirteen_unit_price', 'line_thirteen_total_price',
                  'line_fourteen_bike_name', 'line_fourteen_part_number', 'line_fourteen_part_name',
                  'line_fourteen_quantity',
                  'line_fourteen_unit_price', 'line_fourteen_total_price',
                  'line_fifteen_bike_name', 'line_fifteen_part_number', 'line_fifteen_part_name',
                  'line_fifteen_quantity',
                  'line_fifteen_unit_price', 'line_fifteen_total_price',

                  'line_sixteen_bike_name', 'line_sixteen_part_number', 'line_sixteen_part_name',
                  'line_sixteen_quantity',
                  'line_sixteen_unit_price', 'line_sixteen_total_price',
                  'line_seventeen_bike_name', 'line_seventeen_part_number', 'line_seventeen_part_name',
                  'line_seventeen_quantity',
                  'line_seventeen_unit_price', 'line_seventeen_total_price',
                  'line_eighteen_bike_name', 'line_eighteen_part_number', 'line_eighteen_part_name',
                  'line_eighteen_quantity',
                  'line_eighteen_unit_price', 'line_eighteen_total_price',
                  'line_nineteen_bike_name', 'line_nineteen_part_number', 'line_nineteen_part_name',
                  'line_nineteen_quantity',
                  'line_nineteen_unit_price', 'line_nineteen_total_price',
                  'line_twenty_bike_name', 'line_twenty_part_number', 'line_twenty_part_name',
                  'line_twenty_quantity',
                  'line_twenty_unit_price', 'line_twenty_total_price',
                  'line_twentyone_bike_name', 'line_twentyone_part_number', 'line_twentyone_part_name',
                  'line_twentyone_quantity', 'line_twentyone_unit_price', 'line_twentyone_total_price',
                  'line_twentytwo_bike_name', 'line_twentytwo_part_number', 'line_twentytwo_part_name',
                  'line_twentytwo_quantity', 'line_twentytwo_unit_price', 'line_twentytwo_total_price',
                  'line_twentythree_bike_name', 'line_twentythree_part_number', 'line_twentythree_part_name',
                  'line_twentythree_quantity', 'line_twentythree_unit_price', 'line_twentythree_total_price',
                  'line_twentyfour_bike_name', 'line_twentyfour_part_number', 'line_twentyfour_part_name',
                  'line_twentyfour_quantity', 'line_twentyfour_unit_price', 'line_twentyfour_total_price',
                  'line_twentyfive_bike_name', 'line_twentyfive_part_number', 'line_twentyfive_part_name',
                  'line_twentyfive_quantity', 'line_twentyfive_unit_price', 'line_twentyfive_total_price',

                  'line_twentysix_bike_name', 'line_twentysix_part_number', 'line_twentysix_part_name',
                  'line_twentysix_quantity', 'line_twentysix_unit_price', 'line_twentysix_total_price',
                  'line_twentyseven_bike_name', 'line_twentyseven_part_number', 'line_twentyseven_part_name',
                  'line_twentyseven_quantity', 'line_twentyseven_unit_price', 'line_twentyseven_total_price',
                  'line_twentyeight_bike_name', 'line_twentyeight_part_number', 'line_twentyeight_part_name',
                  'line_twentyeight_quantity', 'line_twentyeight_unit_price', 'line_twentyeight_total_price',
                  'line_twentynine_bike_name', 'line_twentynine_part_number', 'line_twentynine_part_name',
                  'line_twentynine_quantity', 'line_twentynine_unit_price', 'line_twentynine_total_price',
                  'line_thirty_bike_name', 'line_thirty_part_number', 'line_thirty_part_name', 'line_thirty_quantity',
                  'line_thirty_unit_price', 'line_thirty_total_price',

                  'total', 'paid', 'invoice_type'
                  ]

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError(required)
        return name

    def clean_line_one_bike_name(self):
        line_one_bike_name = self.cleaned_data.get('line_one_bike_name')
        if not line_one_bike_name:
            raise forms.ValidationError(required)
        return line_one_bike_name

    def clean_line_one_quantity(self):
        line_one_quantity = self.cleaned_data.get('line_one_quantity')
        if not line_one_quantity:
            raise forms.ValidationError(required)
        return line_one_quantity


class InvoiceSearchForm(forms.ModelForm):
    generate_invoice = forms.BooleanField(required=False)

    class Meta:
        model = Invoice
        fields = ['invoice_number', 'name', 'generate_invoice']
        fields = '__all__'
        exclude = ()


class InvoiceUpdateForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
        exclude = ()
        fields = ['name', 'phone_number', 'invoice_date', 'invoice_number',
                  'line_one_bike_name', 'line_one_part_number', 'line_one_part_name', 'line_one_quantity',
                  'line_one_unit_price', 'line_one_total_price',
                  'line_two_bike_name', 'line_two_part_number', 'line_two_part_name', 'line_two_quantity',
                  'line_two_unit_price', 'line_two_total_price',
                  'line_three_bike_name', 'line_three_part_number', 'line_three_part_name', 'line_three_quantity',
                  'line_three_unit_price', 'line_three_total_price',
                  'line_four_bike_name', 'line_four_part_number', 'line_four_part_name', 'line_four_quantity',
                  'line_four_unit_price', 'line_four_total_price',
                  'line_five_bike_name', 'line_five_part_number', 'line_five_part_name', 'line_five_quantity',
                  'line_five_unit_price', 'line_five_total_price',

                  'line_six_bike_name', 'line_six_part_number', 'line_six_part_name', 'line_six_quantity',
                  'line_six_unit_price', 'line_six_total_price',
                  'line_seven_bike_name', 'line_seven_part_number', 'line_seven_part_name', 'line_seven_quantity',
                  'line_seven_unit_price', 'line_seven_total_price',
                  'line_eight_bike_name', 'line_eight_part_number', 'line_eight_part_name', 'line_eight_quantity',
                  'line_eight_unit_price', 'line_eight_total_price',
                  'line_nine_bike_name', 'line_nine_part_number', 'line_nine_part_name', 'line_nine_quantity',
                  'line_nine_unit_price', 'line_nine_total_price',
                  'line_ten_bike_name', 'line_ten_part_number', 'line_ten_part_name', 'line_ten_quantity',
                  'line_ten_unit_price', 'line_ten_total_price',

                  'line_eleven_bike_name', 'line_eleven_part_number', 'line_eleven_part_name', 'line_eleven_quantity',
                  'line_eleven_unit_price', 'line_eleven_total_price',
                  'line_twelve_bike_name', 'line_twelve_part_number', 'line_twelve_part_name', 'line_twelve_quantity',
                  'line_twelve_unit_price', 'line_twelve_total_price',
                  'line_thirteen_bike_name', 'line_thirteen_part_number', 'line_thirteen_part_name',
                  'line_thirteen_quantity',
                  'line_thirteen_unit_price', 'line_thirteen_total_price',
                  'line_fourteen_bike_name', 'line_fourteen_part_number', 'line_fourteen_part_name',
                  'line_fourteen_quantity',
                  'line_fourteen_unit_price', 'line_fourteen_total_price',
                  'line_fifteen_bike_name', 'line_fifteen_part_number', 'line_fifteen_part_name',
                  'line_fifteen_quantity',
                  'line_fifteen_unit_price', 'line_fifteen_total_price',

                  'line_sixteen_bike_name', 'line_sixteen_part_number', 'line_sixteen_part_name',
                  'line_sixteen_quantity',
                  'line_sixteen_unit_price', 'line_sixteen_total_price',
                  'line_seventeen_bike_name', 'line_seventeen_part_number', 'line_seventeen_part_name',
                  'line_seventeen_quantity',
                  'line_seventeen_unit_price', 'line_seventeen_total_price',
                  'line_eighteen_bike_name', 'line_eighteen_part_number', 'line_eighteen_part_name',
                  'line_eighteen_quantity',
                  'line_eighteen_unit_price', 'line_eighteen_total_price',
                  'line_nineteen_bike_name', 'line_nineteen_part_number', 'line_nineteen_part_name',
                  'line_nineteen_quantity',
                  'line_nineteen_unit_price', 'line_nineteen_total_price',
                  'line_twenty_bike_name', 'line_twenty_part_number', 'line_twenty_part_name', 'line_twenty_quantity',
                  'line_twenty_unit_price', 'line_twenty_total_price',
                  'line_twentyone_bike_name', 'line_twentyone_part_number', 'line_twentyone_part_name',
                  'line_twentyone_quantity', 'line_twentyone_unit_price', 'line_twentyone_total_price',
                  'line_twentytwo_bike_name', 'line_twentytwo_part_number', 'line_twentytwo_part_name',
                  'line_twentytwo_quantity', 'line_twentytwo_unit_price', 'line_twentytwo_total_price',
                  'line_twentythree_bike_name', 'line_twentythree_part_number', 'line_twentythree_part_name',
                  'line_twentythree_quantity', 'line_twentythree_unit_price', 'line_twentythree_total_price',
                  'line_twentyfour_bike_name', 'line_twentyfour_part_number', 'line_twentyfour_part_name',
                  'line_twentyfour_quantity', 'line_twentyfour_unit_price', 'line_twentyfour_total_price',
                  'line_twentyfive_bike_name', 'line_twentyfive_part_number', 'line_twentyfive_part_name',
                  'line_twentyfive_quantity', 'line_twentyfive_unit_price', 'line_twentyfive_total_price',

                  'line_twentysix_bike_name', 'line_twentysix_part_number', 'line_twentysix_part_name',
                  'line_twentysix_quantity', 'line_twentysix_unit_price', 'line_twentysix_total_price',
                  'line_twentyseven_bike_name', 'line_twentyseven_part_number', 'line_twentyseven_part_name',
                  'line_twentyseven_quantity', 'line_twentyseven_unit_price', 'line_twentyseven_total_price',
                  'line_twentyeight_bike_name', 'line_twentyeight_part_number', 'line_twentyeight_part_name',
                  'line_twentyeight_quantity', 'line_twentyeight_unit_price', 'line_twentyeight_total_price',
                  'line_twentynine_bike_name', 'line_twentynine_part_number', 'line_twentynine_part_name',
                  'line_twentynine_quantity', 'line_twentynine_unit_price', 'line_twentynine_total_price',
                  'line_thirty_bike_name', 'line_thirty_part_number', 'line_thirty_part_name', 'line_thirty_quantity',
                  'line_thirty_unit_price', 'line_thirty_total_price',

                  'total', 'paid', 'invoice_type'
                  ]

        def clean_invoice_number(self):
            invoice_number = self.cleaned_data.get('invoice_number')
            if not invoice_number:
                raise forms.ValidationError(required)
            return invoice_number

        def clean_name(self):
            name = self.cleaned_data.get('name')
            if not name:
                raise forms.ValidationError(required)
            return name

        def clean_line_one_bike_name(self):
            line_one_bike_name = self.cleaned_data.get('line_one_bike_name')
            if not line_one_bike_name:
                raise forms.ValidationError(required)
            return line_one_bike_name

        def clean_line_one_quantity(self):
            line_one_quantity = self.cleaned_data.get('line_one_quantity')
            if not line_one_quantity:
                raise forms.ValidationError(required)
            return line_one_quantity

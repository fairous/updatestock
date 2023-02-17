from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

from .forms import InvoiceForm, InvoiceSearchForm, InvoiceUpdateForm
from .models import Invoice
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def home(request):
    title = 'Welcome: This is the Home Page'
    context = {
        "title": title,
    }
    return redirect('/list_items')


# return render(request, "home.html", context)

@csrf_exempt
@login_required
def list_items(request):
    header = 'LIST OF ITEMS'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        "header": header,
        "queryset": queryset,
        "form": form,
    }
    if request.method == 'POST':
        queryset = Stock.objects.filter(
                                        # bike_name__icontains=form['bike_name'].value(),
                                        part_number__icontains=form['part_number'].value(),
                                        part_name__icontains=form['part_name'].value(),
                                        )

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['BRAND', 'BIKE', 'PART NUMBER', 'PART NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.brand_name, stock.bike_name, stock.part_number, stock.part_name, stock.quantity])
            return response

        context = {
            "form": form,
            "header": header,
            "queryset": queryset,
        }
    return render(request, "list_items.html", context)

@csrf_exempt
@login_required
def add_items(request):
    header = 'ADD ITEMS'
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Saved Successfully')
        return redirect('/list_items')
    context = {
        "form": form,
        "header": header,
        "title": "Add Item",
    }
    return render(request, "add_items.html", context)

@csrf_exempt
def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
        messages.success(request, 'Updated Successfully')
        return redirect('/list_items')

    context = {
        'form': form
    }
    return render(request, 'add_items.html', context)

@csrf_exempt
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Deleted Successfully')
        return redirect('/list_items')
    return render(request, 'delete_items.html')

@csrf_exempt
def stock_details(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "title": queryset.bike_name,
        "queryset": queryset,
    }
    return render(request, "stock_details.html", context)

@csrf_exempt
def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity -= instance.issue_quantity
        # instance.issue_by = str(request.user)
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(
            instance.part_name) + "s now left in Store")
        instance.save()
        issue_history = StockHistory(
            id=instance.id,
            last_updated=instance.last_updated,
            brand_name=instance.brand_name,
            bike_name=instance.bike_name,
            part_name=instance.part_name,
            quantity=instance.quantity,
            # receive_to=instance.issue_to,
            issue_by=instance.issue_by,
            issue_quantity=instance.issue_quantity,
            timestamp=instance.timestamp
        )
        issue_history.save()

        return redirect('/stock_details/' + str(instance.id))

    # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": 'Issue ' + str(queryset.part_name),
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)

@csrf_exempt
def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity += instance.receive_quantity
        messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(
            instance.part_name) + "s now in Store")
        instance.save()
        receive_history = StockHistory(
            id=instance.id,
            last_updated=instance.last_updated,
            brand_name=instance.brand_name,
            bike_name=instance.bike_name,
            part_name=instance.part_name,
            quantity=instance.quantity,
            # receive_by=instance.receive_to,
            receive_by=instance.receive_by,
            receive_quantity=instance.receive_quantity,
            timestamp=instance.timestamp,
        )
        receive_history.save()

        return redirect('/stock_details/' + str(instance.id))
    # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": 'Receive ' + str(queryset.part_name),
        "instance": queryset,
        "form": form,
        "username": 'Receive By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)

@csrf_exempt
def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.part_name) + " is updated to " + str(
            instance.reorder_level))

        return redirect("/list_items")
    context = {
        "instance": queryset,
        "form": form,
    }
    return render(request, "add_items.html", context)

@csrf_exempt
@login_required
def list_history(request):
    header = 'HISTORY DATA'
    queryset = StockHistory.objects.all()
    form = StockHistorySearchForm(request.POST or None)
    context = {
        "header": header,
        "queryset": queryset,
        "form": form,
    }

    if request.method == 'POST':
        bike_name = form['bike_name'].value()
        queryset = StockHistory.objects.filter(part_name__icontains=form['part_name'].value()
                                               #  last_updated__range=[
                                               #     form['start_date'].value(),
                                               #    form['end_date'].value()
                                               # ]
                                               )

        if (bike_name != ''):
            queryset = queryset.filter(bike_name=bike_name)

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
            writer = csv.writer(response)
            writer.writerow(
                ['BIKE',
                 'PART NAME',
                 'QUANTITY',
                 'ISSUE QUANTITY',
                 'RECEIVE QUANTITY',
                 'RECEIVE BY',
                 'ISSUE BY',
                 'LAST UPDATED'])
            instance = queryset
            for stock in instance:
                writer.writerow(
                    [stock.bike_name,
                     stock.brand_name,
                     stock.part_name,
                     stock.quantity,
                     stock.issue_quantity,
                     stock.receive_quantity,
                     stock.receive_by,
                     stock.issue_by,
                     stock.last_updated])
            return response

    context = {
        "form": form,
        "header": header,
        "queryset": queryset,
    }
    return render(request, "list_history.html", context)




# For Report Lab
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.pagesizes import landscape
# from reportlab.platypus import Image
# from reportlab.lib.units import inch


# End for report lab


# def home(request):
#     title = 'welcome to home '
#     context = {
#         "title": title,
#     }
#     return render(request, "home.html", context)

@csrf_exempt
def add_invoice(request):
    header = 'NEW INVOICE'
    form = InvoiceForm(request.POST or None)
    total_invoices = Invoice.objects.count()
    queryset = Invoice.objects.order_by('-invoice_date')[:8]

    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('/list_invoice')
    context = {
        "form": form,
        "header": header,
        # "title": "New Invoice",
        "total_invoices": total_invoices,
        "queryset": queryset,
    }
    return render(request, "entry.html", context)

@csrf_exempt
def list_invoice(request):
    header = 'INVOICE LIST'
    # title = 'List of Invoices'
    queryset = Invoice.objects.all()
    form = InvoiceSearchForm(request.POST or None)
    context = {
        # "title": title,
        "header": header,
        "queryset": queryset,
        "form": form,
    }

    if request.method == 'POST':
        queryset = Invoice.objects.filter(invoice_number__icontains=form['invoice_number'].value(),
                                          name__icontains=form['name'].value()
                                          )
        context = {
            "form": form,
            "header": header,
            "title": title,
            "queryset": queryset,
        }
        if form['generate_invoice'].value() == True:
            instance = queryset
            data_file = instance
            num_of_invoices = len(queryset)
            message = str(num_of_invoices) + " invoices successfully generated."
            messages.success(request, message)

            def import_data(data_file):
                invoice_data = data_file
                for row in invoice_data:
                    invoice_type = row.invoice_type
                    invoice_number = row.invoice_number
                    invoice_date = row.invoice_date
                    name = row.name
                    phone_number = row.phone_number

                    line_one_bike_name = row.line_one_bike_name
                    line_one_part_number = row.line_one_part_number
                    line_one_part_name = row.line_one_part_name
                    line_one_quantity = row.line_one_quantity
                    line_one_unit_price = row.line_one_unit_price
                    line_one_total_price = row.line_one_total_price

                    line_two_bike_name = row.line_two_bike_name
                    line_two_part_number = row.line_two_part_number
                    line_two_part_name = row.line_two_part_name
                    line_two_quantity = row.line_two_quantity
                    line_two_unit_price = row.line_two_unit_price
                    line_two_total_price = row.line_two_total_price

                    line_three_bike_name = row.line_three_bike_name
                    line_three_part_number = row.line_three_part_number
                    line_three_part_name = row.line_three_part_name
                    line_three_quantity = row.line_three_quantity
                    line_three_unit_price = row.line_three_unit_price
                    line_three_total_price = row.line_three_total_price

                    line_four_bike_name = row.line_four_bike_name
                    line_four_part_number = row.line_four_part_number
                    line_four_part_name = row.line_four_part_name
                    line_four_quantity = row.line_four_quantity
                    line_four_unit_price = row.line_four_unit_price
                    line_four_total_price = row.line_four_total_price

                    line_five_bike_name = row.line_five_bike_name
                    line_five_part_number = row.line_five_part_number
                    line_five_part_name = row.line_five_part_name
                    line_five_quantity = row.line_five_quantity
                    line_five_unit_price = row.line_five_unit_price
                    line_five_total_price = row.line_five_total_price

                    line_six_bike_name = row.line_six_bike_name
                    line_six_part_number = row.line_six_part_number
                    line_six_part_name = row.line_six_part_name
                    line_six_quantity = row.line_six_quantity
                    line_six_unit_price = row.line_six_unit_price
                    line_six_total_price = row.line_six_total_price

                    line_seven_bike_name = row.line_seven_bike_name
                    line_seven_part_number = row.line_seven_part_number
                    line_seven_part_name = row.line_seven_part_name
                    line_seven_quantity = row.line_seven_quantity
                    line_seven_unit_price = row.line_seven_unit_price
                    line_seven_total_price = row.line_seven_total_price

                    line_eight_bike_name = row.line_eight_bike_name
                    line_eight_part_number = row.line_eight_part_number
                    line_eight_part_name = row.line_eight_part_name
                    line_eight_quantity = row.line_eight_quantity
                    line_eight_unit_price = row.line_eight_unit_price
                    line_eight_total_price = row.line_eight_total_price

                    line_nine_bike_name = row.line_nine_bike_name
                    line_nine_part_number = row.line_nine_part_number
                    line_nine_part_name = row.line_nine_part_name
                    line_nine_quantity = row.line_nine_quantity
                    line_nine_unit_price = row.line_nine_unit_price
                    line_nine_total_price = row.line_nine_total_price

                    line_ten_bike_name = row.line_ten_bike_name
                    line_ten_part_number = row.line_ten_part_number
                    line_ten_part_name = row.line_ten_part_name
                    line_ten_quantity = row.line_ten_quantity
                    line_ten_unit_price = row.line_ten_unit_price
                    line_ten_total_price = row.line_ten_total_price

                    line_eleven_bike_name = row.line_eleven_bike_name
                    line_eleven_part_number = row.line_eleven_part_number
                    line_eleven_part_name = row.line_eleven_part_name
                    line_eleven_quantity = row.line_eleven_quantity
                    line_eleven_unit_price = row.line_eleven_unit_price
                    line_eleven_total_price = row.line_eleven_total_price

                    line_twelve_bike_name = row.line_twelve_bike_name
                    line_twelve_part_number = row.line_twelve_part_number
                    line_twelve_part_name = row.line_twelve_part_name
                    line_twelve_quantity = row.line_twelve_quantity
                    line_twelve_unit_price = row.line_twelve_unit_price
                    line_twelve_total_price = row.line_twelve_total_price

                    line_thirteen_bike_name = row.line_thirteen_bike_name
                    line_thirteen_part_number = row.line_thirteen_part_number
                    line_thirteen_part_name = row.line_thirteen_part_name
                    line_thirteen_quantity = row.line_thirteen_quantity
                    line_thirteen_unit_price = row.line_thirteen_unit_price
                    line_thirteen_total_price = row.line_thirteen_total_price

                    line_fourteen_bike_name = row.line_fourteen_bike_name
                    line_fourteen_part_number = row.line_fourteen_part_number
                    line_fourteen_part_name = row.line_fourteen_part_name
                    line_fourteen_quantity = row.line_fourteen_quantity
                    line_fourteen_unit_price = row.line_fourteen_unit_price
                    line_fourteen_total_price = row.line_fourteen_total_price

                    line_fifteen_bike_name = row.line_fifteen_bike_name
                    line_fifteen_part_number = row.line_fifteen_part_number
                    line_fifteen_part_name = row.line_fifteen_part_name
                    line_fifteen_quantity = row.line_fifteen_quantity
                    line_fifteen_unit_price = row.line_fifteen_unit_price
                    line_fifteen_total_price = row.line_fifteen_total_price

                    line_sixteen_bike_name = row.line_sixteen_bike_name
                    line_sixteen_part_number = row.line_sixteen_part_number
                    line_sixteen_part_name = row.line_sixteen_part_name
                    line_sixteen_quantity = row.line_sixteen_quantity
                    line_sixteen_unit_price = row.line_sixteen_unit_price
                    line_sixteen_total_price = row.line_sixteen_total_price

                    line_seventeen_bike_name = row.line_seventeen_bike_name
                    line_seventeen_part_number = row.line_seventeen_part_number
                    line_seventeen_part_name = row.line_seventeen_part_name
                    line_seventeen_quantity = row.line_seventeen_quantity
                    line_seventeen_unit_price = row.line_seventeen_unit_price
                    line_seventeen_total_price = row.line_seventeen_total_price

                    line_eighteen_bike_name = row.line_eighteen_bike_name
                    line_eighteen_part_number = row.line_eighteen_part_number
                    line_eighteen_part_name = row.line_eighteen_part_name
                    line_eighteen_quantity = row.line_eighteen_quantity
                    line_eighteen_unit_price = row.line_eighteen_unit_price
                    line_eighteen_total_price = row.line_eighteen_total_price

                    line_nineteen_bike_name = row.line_nineteen_bike_name
                    line_nineteen_part_number = row.line_nineteen_part_number
                    line_nineteen_part_name = row.line_nineteen_part_name
                    line_nineteen_quantity = row.line_nineteen_quantity
                    line_nineteen_unit_price = row.line_nineteen_unit_price
                    line_nineteen_total_price = row.line_nineteen_total_price

                    line_twenty_bike_name = row.line_twenty_bike_name
                    line_twenty_part_number = row.line_twenty_part_number
                    line_twenty_part_name = row.line_twenty_part_name
                    line_twenty_quantity = row.line_twenty_quantity
                    line_twenty_unit_price = row.line_twenty_unit_price
                    line_twenty_total_price = row.line_twenty_total_price

                    line_twentyone_bike_name = row.line_twentyone_bike_name
                    line_twentyone_part_number = row.line_twentyone_part_number
                    line_twentyone_part_name = row.line_twentyone_part_name
                    line_twentyone_quantity = row.line_twentyone_quantity
                    line_twentyone_unit_price = row.line_twentyone_unit_price
                    line_twentyone_total_price = row.line_twentyone_total_price

                    line_twentytwo_bike_name = row.line_twentytwo_bike_name
                    line_twentytwo_part_number = row.line_twentytwo_part_number
                    line_twentytwo_part_name = row.line_twentytwo_part_name
                    line_twentytwo_quantity = row.line_twentytwo_quantity
                    line_twentytwo_unit_price = row.line_twentytwo_unit_price
                    line_twentytwo_total_price = row.line_twentytwo_total_price

                    line_twentythree_bike_name = row.line_twentythree_bike_name
                    line_twentythree_part_number = row.line_twentythree_part_number
                    line_twentythree_part_name = row.line_twentythree_part_name
                    line_twentythree_quantity = row.line_twentythree_quantity
                    line_twentythree_unit_price = row.line_twentythree_unit_price
                    line_twentythree_total_price = row.line_twentythree_total_price

                    line_twentyfour_bike_name = row.line_twentyfour_bike_name
                    line_twentyfour_part_number = row.line_twentyfour_part_number
                    line_twentyfour_part_name = row.line_twentyfour_part_name
                    line_twentyfour_quantity = row.line_twentyfour_quantity
                    line_twentyfour_unit_price = row.line_twentyfour_unit_price
                    line_twentyfour_total_price = row.line_twentyfour_total_price

                    line_twentyfive_bike_name = row.line_twentyfive_bike_name
                    line_twentyfive_part_number = row.line_twentyfive_part_number
                    line_twentyfive_part_name = row.line_twentyfive_part_name
                    line_twentyfive_quantity = row.line_twentyfive_quantity
                    line_twentyfive_unit_price = row.line_twentyfive_unit_price
                    line_twentyfive_total_price = row.line_twentyfive_total_price

                    line_twentysix_bike_name = row.line_twentysix_bike_name
                    line_twentysix_part_number = row.line_twentysix_part_number
                    line_twentysix_part_name = row.line_twentysix_part_name
                    line_twentysix_quantity = row.line_twentysix_quantity
                    line_twentysix_unit_price = row.line_twentysix_unit_price
                    line_twentysix_total_price = row.line_twentysix_total_price

                    line_twentyseven_bike_name = row.line_twentyseven_bike_name
                    line_twentyseven_part_number = row.line_twentyseven_part_number
                    line_twentyseven_part_name = row.line_twentyseven_part_name
                    line_twentyseven_quantity = row.line_twentyseven_quantity
                    line_twentyseven_unit_price = row.line_twentyseven_unit_price
                    line_twentyseven_total_price = row.line_twentyseven_total_price

                    line_twentyeight_bike_name = row.line_twentyeight_bike_name
                    line_twentyeight_part_number = row.line_twentyeight_part_number
                    line_twentyeight_part_name = row.line_twentyeight_part_name
                    line_twentyeight_quantity = row.line_twentyeight_quantity
                    line_twentyeight_unit_price = row.line_twentyeight_unit_price
                    line_twentyeight_total_price = row.line_twentyeight_total_price

                    line_twentynine_bike_name = row.line_twentynine_bike_name
                    line_twentynine_part_number = row.line_twentynine_part_number
                    line_twentynine_part_name = row.line_twentynine_part_name
                    line_twentynine_quantity = row.line_twentynine_quantity
                    line_twentynine_unit_price = row.line_twentynine_unit_price
                    line_twentynine_total_price = row.line_twentynine_total_price

                    line_thirty_bike_name = row.line_thirty_bike_name
                    line_thirty_part_number = row.line_thirty_part_number
                    line_thirty_part_name = row.line_thirty_part_name
                    line_thirty_quantity = row.line_thirty_quantity
                    line_thirty_unit_price = row.line_thirty_unit_price
                    line_thirty_total_price = row.line_thirty_total_price

                    total = row.total
                    pdf_file_name = str(invoice_number) + '_' + str(name) + '.pdf'
                    generate_invoice(str(name), str(invoice_number), str(line_one_bike_name),
                                     str(line_one_part_number), str(line_one_part_name),
                                     str(line_one_quantity), str(line_one_unit_price), str(line_one_total_price),
                                     str(line_two_bike_name), str(line_two_part_number), str(line_two_part_name),
                                     str(line_two_quantity), str(line_two_unit_price), str(line_two_total_price),
                                     str(line_three_bike_name), str(line_three_part_number), str(line_three_part_name),
                                     str(line_three_quantity), str(line_three_unit_price), str(line_three_total_price),
                                     str(line_four_bike_name), str(line_four_part_number), str(line_four_part_name),
                                     str(line_four_quantity), str(line_four_unit_price), str(line_four_total_price),
                                     str(line_five_bike_name), str(line_five_part_number), str(line_five_part_name),
                                     str(line_five_quantity), str(line_five_unit_price), str(line_five_total_price),
                                     str(line_six_bike_name), str(line_six_part_number), str(line_six_part_name),
                                     str(line_six_quantity), str(line_six_unit_price), str(line_six_total_price),
                                     str(line_seven_bike_name), str(line_seven_part_number), str(line_seven_part_name),
                                     str(line_seven_quantity), str(line_seven_unit_price), str(line_seven_total_price),
                                     str(line_eight_bike_name), str(line_eight_part_number), str(line_eight_part_name),
                                     str(line_eight_quantity), str(line_eight_unit_price), str(line_eight_total_price),
                                     str(line_nine_bike_name), str(line_nine_part_number), str(line_nine_part_name),
                                     str(line_nine_quantity), str(line_nine_unit_price), str(line_nine_total_price),
                                     str(line_ten_bike_name), str(line_ten_part_number), str(line_ten_part_name),
                                     str(line_ten_quantity), str(line_ten_unit_price), str(line_ten_total_price),
                                     str(line_eleven_bike_name), str(line_eleven_part_number), str(line_eleven_part_name),
                                     str(line_eleven_quantity), str(line_eleven_unit_price),str(line_eleven_total_price),
                                     str(line_twelve_bike_name), str(line_twelve_part_number),str(line_twelve_part_name),
                                     str(line_twelve_quantity), str(line_twelve_unit_price),str(line_twelve_total_price),
                                     str(line_thirteen_bike_name), str(line_thirteen_part_number),str(line_thirteen_part_name),
                                     str(line_thirteen_quantity), str(line_thirteen_unit_price),str(line_thirteen_total_price),
                                     str(line_fourteen_bike_name), str(line_fourteen_part_number),str(line_fourteen_part_name),
                                     str(line_fourteen_quantity), str(line_fourteen_unit_price),str(line_fourteen_total_price),
                                     str(line_fifteen_bike_name), str(line_fifteen_part_number),str(line_fifteen_part_name),
                                     str(line_fifteen_quantity), str(line_fifteen_unit_price),str(line_fifteen_total_price),str(line_sixteen_bike_name), str(line_sixteen_part_number),
                                     str(line_sixteen_part_name),str(line_sixteen_quantity), str(line_sixteen_unit_price),
                                     str(line_sixteen_total_price),str(line_seventeen_bike_name), str(line_seventeen_part_number),
                                     str(line_seventeen_part_name),str(line_seven_quantity), str(line_seventeen_unit_price),
                                     str(line_seventeen_total_price),str(line_eighteen_bike_name), str(line_eighteen_part_number),
                                     str(line_eighteen_part_name), str(line_eighteen_quantity), str(line_eighteen_unit_price),
                                     str(line_eighteen_total_price), str(line_nineteen_bike_name), str(line_nineteen_part_number),
                                     str(line_nineteen_part_name), str(line_nineteen_quantity), str(line_nineteen_unit_price),
                                     str(line_nineteen_total_price),str(line_twenty_bike_name), str(line_twenty_part_number),
                                     str(line_twenty_part_name),str(line_twenty_quantity), str(line_twenty_unit_price),
                                     str(line_twenty_total_price),str(line_twentyone_bike_name), str(line_twentyone_part_number),
                                     str(line_twentyone_part_name),str(line_twentyone_quantity), str(line_twentyone_unit_price),
                                     str(line_twentyone_total_price),str(line_twentytwo_bike_name), str(line_twentytwo_part_number),
                                     str(line_twentytwo_part_name),str(line_twentytwo_quantity), str(line_twentytwo_unit_price),
                                     str(line_twentytwo_total_price),str(line_twentythree_bike_name), str(line_twentythree_part_number), str(line_twentythree_part_name),
                                     str(line_twentythree_quantity), str(line_twentythree_unit_price), str(line_twentythree_total_price),
                                     str(line_twentyfour_bike_name), str(line_twentyfour_part_number), str(line_twentyfour_part_name),
                                     str(line_twentyfour_quantity), str(line_twentyfour_unit_price), str(line_twentyfour_total_price),
                                     str(line_twentyfive_bike_name), str(line_twentyfive_part_number), str(line_twentyfive_part_name),
                                     str(line_twentyfive_quantity), str(line_twentyfive_unit_price), str(line_twentyfive_total_price),
                                     str(line_twentysix_bike_name), str(line_twentysix_part_number), str(line_twentysix_part_name),
                                     str(line_twentysix_quantity), str(line_twentysix_unit_price), str(line_twentysix_total_price),
                                     str(line_twentyseven_bike_name), str(line_twentyseven_part_number), str(line_twentyseven_part_name),
                                     str(line_twentyseven_quantity), str(line_twentyseven_unit_price), str(line_twentyseven_total_price),
                                     str(line_twentyeight_bike_name), str(line_twentyeight_part_number), str(line_twentyeight_part_name),
                                     str(line_twentyeight_quantity), str(line_twentyeight_unit_price), str(line_twentyeight_total_price),
                                     str(line_twentynine_bike_name), str(line_twentynine_part_number), str(line_twentynine_part_name),
                                     str(line_twentynine_quantity), str(line_twentynine_unit_price), str(line_twentynine_total_price),
                                     str(line_thirty_bike_name), str(line_thirty_part_number), str(line_thirty_part_name),
                                     str(line_thirty_quantity), str(line_thirty_unit_price), str(line_thirty_total_price),
                                     str(total), str(phone_number), str(invoice_date), str(invoice_type), pdf_file_name)

            def generate_invoice(name, invoice_number, line_one_bike_name, line_one_part_number, line_one_part_name,
                                 line_one_quantity,
                                 line_one_unit_price, line_one_total_price,
                                 line_two_bike_name, line_two_part_number, line_two_part_name, line_two_quantity,
                                 line_two_unit_price, line_two_total_price,
                                 line_three_bike_name, line_three_part_number, line_three_part_name,
                                 line_three_quantity, line_three_unit_price, line_three_total_price,
                                 line_four_bike_name, line_four_part_number, line_four_part_name,
                                 line_four_quantity,
                                 line_four_unit_price, line_four_total_price,
                                 line_five_bike_name, line_five_part_number, line_five_part_name,
                                 line_five_quantity,
                                 line_five_unit_price, line_five_total_price,
                                 line_six_bike_name,
                                 line_six_part_number, line_six_part_name, line_six_quantity, line_six_unit_price,
                                 line_six_total_price,
                                 line_seven_bike_name, line_seven_part_number, line_seven_part_name,
                                 line_seven_quantity,
                                 line_seven_unit_price, line_seven_total_price,
                                 line_eight_bike_name, line_eight_part_number, line_eight_part_name,
                                 line_eight_quantity,
                                 line_eight_unit_price, line_eight_total_price,
                                 line_nine_bike_name, line_nine_part_number, line_nine_part_name,
                                 line_nine_quantity, line_nine_unit_price, line_nine_total_price,
                                 line_ten_bike_name, line_ten_part_number, line_ten_part_name, line_ten_quantity,
                                 line_ten_unit_price, line_ten_total_price,
                                 line_eleven_bike_name, line_eleven_part_number, line_eleven_part_name,
                                 line_eleven_quantity, line_eleven_unit_price, line_eleven_total_price,
                                 line_twelve_bike_name, line_twelve_part_number, line_twelve_part_name,
                                 line_twelve_quantity,
                                 line_twelve_unit_price, line_twelve_total_price,
                                 line_thirteen_bike_name, line_thirteen_part_number, line_thirteen_part_name,
                                 line_thirteen_quantity,
                                 line_thirteen_unit_price, line_thirteen_total_price,
                                 line_fourteen_bike_name, line_fourteen_part_number, line_fourteen_part_name,
                                 line_fourteen_quantity,
                                 line_fourteen_unit_price, line_fourteen_total_price,
                                 line_fifteen_bike_name, line_fifteen_part_number, line_fifteen_part_name,
                                 line_fifteen_quantity,
                                 line_fifteen_unit_price, line_fifteen_total_price,
                                 line_sixteen_bike_name, line_sixteen_part_number, line_sixteen_part_name,
                                 line_sixteen_quantity,
                                 line_sixteen_unit_price, line_sixteen_total_price,
                                 line_seventeen_bike_name, line_seventeen_part_number, line_seventeen_part_name,
                                 line_seventeen_quantity,
                                 line_seventeen_unit_price, line_seventeen_total_price,
                                 line_eighteen_bike_name, line_eighteen_part_number, line_eighteen_part_name,
                                 line_eighteen_quantity,
                                 line_eighteen_unit_price, line_eighteen_total_price,
                                 line_nineteen_bike_name, line_nineteen_part_number, line_nineteen_part_name,
                                 line_nineteen_quantity,
                                 line_nineteen_unit_price, line_nineteen_total_price,
                                 line_twenty_bike_name, line_twenty_part_number, line_twenty_part_name,
                                 line_twenty_quantity,
                                 line_twenty_unit_price, line_twenty_total_price,
                                 line_twentyone_bike_name, line_twentyone_part_number, line_twentyone_part_name,
                                 line_twentyone_quantity,
                                 line_twentyone_unit_price, line_twentyone_total_price,
                                 line_twentytwo_bike_name, line_twentytwo_part_number, line_twentytwo_part_name,
                                 line_twentytwo_quantity,
                                 line_twentytwo_unit_price, line_twentytwo_total_price,
                                 line_twentythree_bike_name, line_twentythree_part_number, line_twentythree_part_name,
                                 line_twentythree_quantity, line_twentythree_unit_price, line_twentythree_total_price,
                                 line_twentyfour_bike_name, line_twentyfour_part_number, line_twentyfour_part_name,
                                 line_twentyfour_quantity, line_twentyfour_unit_price, line_twentyfour_total_price,
                                 line_twentyfive_bike_name, line_twentyfive_part_number, line_twentyfive_part_name,
                                 line_twentyfive_quantity, line_twentyfive_unit_price, line_twentyfive_total_price,
                                 line_twentysix_bike_name, line_twentysix_part_number, line_twentysix_part_name,
                                 line_twentysix_quantity, line_twentysix_unit_price, line_twentysix_total_price,
                                 line_twentyseven_bike_name, line_twentyseven_part_number, line_twentyseven_part_name,
                                 line_twentyseven_quantity, line_twentyseven_unit_price, line_twentyseven_total_price,
                                 line_twentyeight_bike_name, line_twentyeight_part_number, line_twentyeight_part_name,
                                 line_twentyeight_quantity, line_twentyeight_unit_price, line_twentyeight_total_price,
                                 line_twentynine_bike_name, line_twentynine_part_number, line_twentynine_part_name,
                                 line_twentynine_quantity, line_twentynine_unit_price, line_twentynine_total_price,
                                 line_thirty_bike_name, line_thirty_part_number, line_thirty_part_name,
                                 line_thirty_quantity, line_thirty_unit_price, line_thirty_total_price,
                                 total, phone_number, invoice_date, invoice_type, pdf_file_name):

                c = canvas.Canvas(pdf_file_name)

                # image of seal

                logo = 'logo.png'
                c.drawImage(logo, 15, 780, width=200, height=60)

                c.setFont('Helvetica', 10, leading=None)
                c.setFillColorRGB(0, 0, 1)

                if invoice_type == 'Receipt':
                    c.drawRightString(490, 755, "Receipt Number #:")
                elif invoice_type == 'Proforma Invoice':
                    c.drawRightString(490, 755, "Proforma Invoice #:")
                else:
                    c.drawRightString(490, 755, str(invoice_type) + ':')
                    c.setFont('Helvetica', 10, leading=None)
                invoice_number_string = str('0000' + invoice_number)
                c.setFillColorRGB(0, 0, 0)
                c.drawString(500, 755, invoice_number_string)

                c.setFont('Helvetica', 10, leading=None)
                c.setFillColorRGB(0, 0, 1)
                c.drawRightString(490, 735, "Date:")
                c.setFont('Helvetica', 10, leading=None)
                c.setFillColorRGB(0, 0, 0)
                c.drawString(500, 735, invoice_date)

                c.setFont('Helvetica', 10, leading=None)
                c.setFillColorRGB(0, 0, 1)
                c.drawRightString(490, 715, "Amount:")
                c.setFont('Helvetica-Bold', 10, leading=None)
                c.setFillColorRGB(0, 0, 0)
                c.drawString(500, 715, 'Rs' + total)

                c.setFont('Helvetica', 10, leading=None)
                c.setFillColorRGB(0, 0, 1)
                c.drawRightString(100, 740, "To:")
                c.setFont('Helvetica', 10, leading=None)
                c.setFillColorRGB(0, 0, 0)
                c.drawString(110, 740, name)

                c.setFont('Helvetica', 10, leading=None)
                c.setFillColorRGB(0, 0, 1)
                c.drawRightString(100, 720, "Phone #:")
                c.setFillColorRGB(0, 0, 0)
                c.setFont('Helvetica', 10, leading=None)
                c.drawString(110, 720, phone_number)

                c.setFont('Helvetica-Bold', 14, leading=None)
                # c.setFillColorRGB(0, 0, 1)
                # c.drawCentredString(310, 580, str(invoice_type))
                c.setFillColorRGB(0, 0, 0)
                # c.drawCentredString(110, 560, "Particulars:")
                # c.drawCentredString(295, 595, "_____________________________________________________________________")
                # c.drawCentredString(295, 575, "_____________________________________________________________________")
                # c.drawCentredString(295, 555, "_____________________________________________________________________")
                # c.drawCentredString(295, 535, "_____________________________________________________________________")
                # c.drawCentredString(295, 515, "_____________________________________________________________________")
                # c.drawCentredString(295, 495, "_____________________________________________________________________")
                # c.drawCentredString(295, 475, "_____________________________________________________________________")
                # c.drawCentredString(295, 455, "_____________________________________________________________________")
                # c.drawCentredString(295, 435, "_____________________________________________________________________")
                # c.drawCentredString(295, 415, "_____________________________________________________________________")
                # c.drawCentredString(295, 395, "_____________________________________________________________________")

                c.line(28, 75, 28, 695)
                c.line(47, 75, 47, 695)
                c.line(117, 75, 117, 695)
                c.line(207, 75, 207, 695)
                c.line(360, 75, 360, 695)
                c.line(425, 75, 425, 695)
                c.line(495, 75, 495, 695)
                c.line(562, 75, 562, 695)

                c.line(28, 695, 562, 695)
                c.line(28, 675, 562, 675)
                c.line(28, 655, 562, 655)
                c.line(28, 635, 562, 635)
                c.line(28, 615, 562, 615)
                c.line(28, 595, 562, 595)
                c.line(28, 575, 562, 575)
                c.line(28, 555, 562, 555)
                c.line(28, 535, 562, 535)
                c.line(28, 515, 562, 515)
                c.line(28, 495, 562, 495)
                c.line(28, 475, 562, 475)
                c.line(28, 455, 562, 455)
                c.line(28, 435, 562, 435)
                c.line(28, 415, 562, 415)
                c.line(28, 395, 562, 395)
                c.line(28, 375, 562, 375)
                c.line(28, 355, 562, 355)
                c.line(28, 335, 562, 335)
                c.line(28, 315, 562, 315)
                c.line(28, 295, 562, 295)
                c.line(28, 275, 562, 275)
                c.line(28, 255, 562, 255)
                c.line(28, 235, 562, 235)
                c.line(28, 215, 562, 215)
                c.line(28, 195, 562, 195)
                c.line(28, 175, 562, 175)
                c.line(28, 155, 562, 155)
                c.line(28, 135, 562, 135)
                c.line(28, 115, 562, 115)
                c.line(28, 95, 562, 95)
                c.line(28, 75, 562, 75)



                # c.grid([inch, 2 * inch, 3 * inch, 4 * inch], [0.5 * inch, inch, 1.5 * inch, 2 * inch, 2.5 * inch])

                c.setFont('Helvetica-Bold', 10, leading=None)
                c.setFillColorRGB(0, 0, 1)
                c.drawString(30, 680, 'NO')
                c.drawString(50, 680, 'BIKE')
                c.drawString(120, 680, 'PART NUMBER')
                c.drawString(210, 680, 'PART NAME')
                c.drawRightString(420, 680, 'QUANTITY')
                c.drawRightString(490, 680, 'UNIT PRICE')
                c.drawString(500, 680, 'LINE TOTAL')

                c.setFont('Helvetica', 10, leading=None)
                c.setFillColorRGB(0, 0, 0)
                c.drawString(32, 660, '1')
                c.drawString(50, 660, line_one_bike_name)
                c.drawString(120, 660, line_one_part_number)
                c.drawString(210, 660, line_one_part_name)
                c.drawRightString(415, 660, line_one_quantity)
                c.drawRightString(485, 660, line_one_unit_price)
                c.drawRightString(555, 660, line_one_total_price)

                if line_two_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 640, '2')
                    c.drawString(50, 640, line_two_bike_name)
                    c.drawString(120, 640, line_two_part_number)
                    c.drawString(210, 640, line_two_part_name)
                    c.drawRightString(415, 640, line_two_quantity)
                    c.drawRightString(485, 640, line_two_unit_price)
                    c.drawRightString(555, 640, line_two_total_price)

                if line_three_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 620, '3')
                    c.drawString(50, 620, line_three_bike_name)
                    c.drawString(120, 620, line_three_part_number)
                    c.drawString(210, 620, line_three_part_name)
                    c.drawRightString(415, 620, line_three_quantity)
                    c.drawRightString(485, 620, line_three_unit_price)
                    c.drawRightString(555, 620, line_three_total_price)

                if line_four_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 600, '4')
                    c.drawString(50, 600, line_four_bike_name)
                    c.drawString(120, 600, line_four_part_number)
                    c.drawString(210, 600, line_four_part_name)
                    c.drawRightString(415, 600, line_four_quantity)
                    c.drawRightString(485, 600, line_four_unit_price)
                    c.drawRightString(555, 600, line_four_total_price)

                if line_five_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 580, '5')
                    c.drawString(50, 580, line_five_bike_name)
                    c.drawString(120, 580, line_five_part_number)
                    c.drawString(210, 580, line_five_part_name)
                    c.drawRightString(415, 580, line_five_quantity)
                    c.drawRightString(485, 580, line_five_unit_price)
                    c.drawRightString(555, 580, line_five_total_price)

                if line_six_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 560, '6')
                    c.drawString(50, 560, line_six_bike_name)
                    c.drawString(120, 560, line_six_part_number)
                    c.drawString(210, 560, line_six_part_name)
                    c.drawRightString(415, 560, line_six_quantity)
                    c.drawRightString(485, 560, line_six_unit_price)
                    c.drawRightString(555, 560, line_six_total_price)

                if line_seven_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 540, '7')
                    c.drawString(50, 540, line_seven_bike_name)
                    c.drawString(120, 540, line_seven_part_number)
                    c.drawString(210, 540, line_seven_part_name)
                    c.drawRightString(415, 540, line_seven_quantity)
                    c.drawRightString(485, 540, line_seven_unit_price)
                    c.drawRightString(555, 540, line_seven_total_price)

                if line_eight_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 520, '8')
                    c.drawString(50, 520, line_eight_bike_name)
                    c.drawString(120, 520, line_eight_part_number)
                    c.drawString(210, 520, line_eight_part_name)
                    c.drawRightString(415, 520, line_eight_quantity)
                    c.drawRightString(485, 520, line_eight_unit_price)
                    c.drawRightString(555, 520, line_eight_total_price)

                if line_nine_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 500, '9')
                    c.drawString(50, 500, line_nine_bike_name)
                    c.drawString(120, 500, line_nine_part_number)
                    c.drawString(210, 500, line_nine_part_name)
                    c.drawRightString(415, 500, line_nine_quantity)
                    c.drawRightString(485, 500, line_nine_unit_price)
                    c.drawRightString(555, 500, line_nine_total_price)

                if line_ten_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 480, '10')
                    c.drawString(50, 480, line_ten_bike_name)
                    c.drawString(120, 480, line_ten_part_number)
                    c.drawString(210, 480, line_ten_part_name)
                    c.drawRightString(415, 480, line_ten_quantity)
                    c.drawRightString(485, 480, line_ten_unit_price)
                    c.drawRightString(555, 480, line_ten_total_price)

                if line_eleven_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 460, '11')
                    c.drawString(50, 460, line_eleven_bike_name)
                    c.drawString(120, 460, line_eleven_part_number)
                    c.drawString(210, 460, line_eleven_part_name)
                    c.drawRightString(415, 460, line_eleven_quantity)
                    c.drawRightString(485, 460, line_eleven_unit_price)
                    c.drawRightString(555, 460, line_eleven_total_price)

                if line_twelve_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 440, '12')
                    c.drawString(50, 440, line_twelve_bike_name)
                    c.drawString(120, 440, line_twelve_part_number)
                    c.drawString(210, 440, line_twelve_part_name)
                    c.drawRightString(415, 440, line_twelve_quantity)
                    c.drawRightString(485, 440, line_twelve_unit_price)
                    c.drawRightString(555, 440, line_twelve_total_price)

                if line_thirteen_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 420, '13')
                    c.drawString(50, 420, line_thirteen_bike_name)
                    c.drawString(120, 420, line_thirteen_part_number)
                    c.drawString(210, 420, line_thirteen_part_name)
                    c.drawRightString(415, 420, line_thirteen_quantity)
                    c.drawRightString(485, 420, line_thirteen_unit_price)
                    c.drawRightString(555, 420, line_thirteen_total_price)

                if line_fourteen_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 400, '14')
                    c.drawString(50, 400, line_fourteen_bike_name)
                    c.drawString(120, 400, line_fourteen_part_number)
                    c.drawString(210, 400, line_fourteen_part_name)
                    c.drawRightString(415, 400, line_fourteen_quantity)
                    c.drawRightString(485, 400, line_fourteen_unit_price)
                    c.drawRightString(555, 400, line_fourteen_total_price)

                if line_fifteen_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32,380, '15')
                    c.drawString(50, 380, line_fifteen_bike_name)
                    c.drawString(120, 380, line_fifteen_part_number)
                    c.drawString(210, 380, line_fifteen_part_name)
                    c.drawRightString(415, 380, line_fifteen_quantity)
                    c.drawRightString(485, 380, line_fifteen_unit_price)
                    c.drawRightString(555, 380, line_fifteen_total_price)

                if line_sixteen_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 360, '16')
                    c.drawString(50, 360, line_sixteen_bike_name)
                    c.drawString(120, 360, line_sixteen_part_number)
                    c.drawString(210, 360, line_sixteen_part_name)
                    c.drawRightString(415, 360, line_sixteen_quantity)
                    c.drawRightString(485, 360, line_sixteen_unit_price)
                    c.drawRightString(555, 360, line_sixteen_total_price)

                if line_seventeen_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 340, '17')
                    c.drawString(50, 340, line_seventeen_bike_name)
                    c.drawString(120, 340, line_seventeen_part_number)
                    c.drawString(210, 340, line_seventeen_part_name)
                    c.drawRightString(415, 340, line_seventeen_quantity)
                    c.drawRightString(485, 340, line_seventeen_unit_price)
                    c.drawRightString(555, 340, line_seventeen_total_price)

                if line_eighteen_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 320, '18')
                    c.drawString(50, 320, line_eighteen_bike_name)
                    c.drawString(120, 320, line_eighteen_part_number)
                    c.drawString(210, 320, line_eighteen_part_name)
                    c.drawRightString(415, 320, line_eighteen_quantity)
                    c.drawRightString(485, 320, line_eighteen_unit_price)
                    c.drawRightString(555, 320, line_eighteen_total_price)

                if line_nineteen_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 300, '19')
                    c.drawString(50, 300, line_nineteen_bike_name)
                    c.drawString(120, 300, line_nineteen_part_number)
                    c.drawString(210, 300, line_nineteen_part_name)
                    c.drawRightString(415, 300, line_nineteen_quantity)
                    c.drawRightString(485, 300, line_nineteen_unit_price)
                    c.drawRightString(555, 300, line_nineteen_total_price)

                if line_twenty_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 280, '20')
                    c.drawString(50, 280, line_twenty_bike_name)
                    c.drawString(120, 280, line_twenty_part_number)
                    c.drawString(210, 280, line_twenty_part_name)
                    c.drawRightString(415, 280, line_twenty_quantity)
                    c.drawRightString(485, 280, line_twenty_unit_price)
                    c.drawRightString(555, 280, line_twenty_total_price)

                if line_twentyone_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 260, '21')
                    c.drawString(50, 260, line_twentyone_bike_name)
                    c.drawString(120, 260, line_twentyone_part_number)
                    c.drawString(210, 260, line_twentyone_part_name)
                    c.drawRightString(415, 260, line_twentyone_quantity)
                    c.drawRightString(485, 260, line_twentyone_unit_price)
                    c.drawRightString(555, 260, line_twentyone_total_price)

                if line_twentytwo_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 240, '22')
                    c.drawString(50, 240, line_twentytwo_bike_name)
                    c.drawString(120, 240, line_twentytwo_part_number)
                    c.drawString(210, 240, line_twentytwo_part_name)
                    c.drawRightString(415, 240, line_twentytwo_quantity)
                    c.drawRightString(485, 240, line_twentytwo_unit_price)
                    c.drawRightString(555, 240, line_twentytwo_total_price)

                if line_twentythree_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 220, '23')
                    c.drawString(50, 220, line_twentythree_bike_name)
                    c.drawString(120, 220, line_twentythree_part_number)
                    c.drawString(210, 220, line_twentythree_part_name)
                    c.drawRightString(415, 220, line_twentythree_quantity)
                    c.drawRightString(485, 220, line_twentythree_unit_price)
                    c.drawRightString(555, 220, line_twentythree_total_price)

                if line_twentyfour_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 200, '24')
                    c.drawString(50, 200, line_twentyfour_bike_name)
                    c.drawString(120, 200, line_twentyfour_part_number)
                    c.drawString(210, 200, line_twentyfour_part_name)
                    c.drawRightString(415, 200, line_twentyfour_quantity)
                    c.drawRightString(485, 200, line_twentyfour_unit_price)
                    c.drawRightString(555, 200, line_twentyfour_total_price)

                if line_twentyfive_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 180, '25')
                    c.drawString(50, 180, line_twentyfive_bike_name)
                    c.drawString(120, 180, line_twentyfive_part_number)
                    c.drawString(210, 180, line_twentyfive_part_name)
                    c.drawRightString(415, 180, line_twentyfive_quantity)
                    c.drawRightString(485, 180, line_twentyfive_unit_price)
                    c.drawRightString(555, 180, line_twentyfive_total_price)

                if line_twentysix_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 160, '26')
                    c.drawString(50, 160, line_twentysix_bike_name)
                    c.drawString(120, 160, line_twentysix_part_number)
                    c.drawString(210, 160, line_twentysix_part_name)
                    c.drawRightString(415, 160, line_twentysix_quantity)
                    c.drawRightString(485, 160, line_twentysix_unit_price)
                    c.drawRightString(555, 160, line_twentysix_total_price)

                if line_twentyseven_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 140, '27')
                    c.drawString(50, 140, line_twentyseven_bike_name)
                    c.drawString(120, 140, line_twentyseven_part_number)
                    c.drawString(210, 140, line_twentyseven_part_name)
                    c.drawRightString(415, 140, line_twentyseven_quantity)
                    c.drawRightString(485, 140, line_twentyseven_unit_price)
                    c.drawRightString(555, 140, line_twentyseven_total_price)

                if line_twentyeight_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 120, '28')
                    c.drawString(50, 120, line_twentyeight_bike_name)
                    c.drawString(120, 120, line_twentyeight_part_number)
                    c.drawString(210, 120, line_twentyeight_part_name)
                    c.drawRightString(415, 120, line_twentyeight_quantity)
                    c.drawRightString(485, 120, line_twentyeight_unit_price)
                    c.drawRightString(555, 120, line_twentyeight_total_price)

                if line_twentynine_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 100, '29')
                    c.drawString(50, 100, line_twentynine_bike_name)
                    c.drawString(120, 100, line_twentynine_part_number)
                    c.drawString(210, 100, line_twentynine_part_name)
                    c.drawRightString(415, 100, line_twentynine_quantity)
                    c.drawRightString(485, 100, line_twentynine_unit_price)
                    c.drawRightString(555, 100, line_twentynine_total_price)

                if line_thirty_bike_name != '':
                    c.setFont('Helvetica', 10, leading=None)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(32, 80, '30')
                    c.drawString(50, 80, line_thirty_bike_name)
                    c.drawString(120, 80, line_thirty_part_number)
                    c.drawString(210, 80, line_thirty_part_name)
                    c.drawRightString(415, 80, line_thirty_quantity)
                    c.drawRightString(485, 80, line_thirty_unit_price)
                    c.drawRightString(555, 80, line_thirty_total_price)



                # TOTAL
                c.setFont('Helvetica-Bold', 12, leading=None)
                c.drawRightString(430, 40, "TOTAL:")
                c.setFont('Helvetica-Bold', 15, leading=None)
                c.drawRightString(554, 40, 'Rs' + total)

                # SIGN
                c.setFont('Helvetica-Bold', 10, leading=None)
                c.drawCentredString(120, 40, "Signed:__________________")
                c.setFont('Helvetica-Bold', 10, leading=None)
                c.drawCentredString(150, 20, 'Manager')

                c.showPage()
                c.save()

            import_data(data_file)

    return render(request, "list_invoice.html", context)

@csrf_exempt
def update_invoice(request, pk):
    queryset = Invoice.objects.get(id=pk)
    form = InvoiceUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = InvoiceUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Saved')
        return redirect('/list_invoice')

    context = {
        'form': form
    }
    return render(request, 'entry.html', context)

@csrf_exempt
def delete_invoice(request, pk):
    queryset = Invoice.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        return redirect('/list_invoice')
    return render(request, 'delete_invoice.html')


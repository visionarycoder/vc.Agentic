# UI Projection Patterns

Generate framework-specific frontend code from service boundary contracts.

## Projection Philosophy

UI projections are generated from the Contract project only. They never reference Service implementations, ensuring UI remains decoupled from backend volatility.

## Vue.js Projections

### Component Generation

```typescript
// Generated from BillingDefinition contract
<template>
  <div class="billing-invoice-view">
    <h2>Invoice {{ invoice?.invoiceNumber }}</h2>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="invoice">
      <p>Amount: {{ formatCurrency(invoice.amount) }}</p>
      <p>Due Date: {{ formatDate(invoice.dueDate) }}</p>
      <button @click="handlePay">Pay Invoice</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useBillingStore } from '@/stores/billing'
import type { Invoice } from '@/types/billing'

const props = defineProps<{
  invoiceId: string
}>()

const store = useBillingStore()
const invoice = ref<Invoice | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

onMounted(async () => {
  loading.value = true
  try {
    invoice.value = await store.getInvoice(props.invoiceId)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

const handlePay = async () => {
  await store.payInvoice(props.invoiceId)
}
</script>
```

### Pinia Store Generation

```typescript
// Generated from IBillingService contract
import { defineStore } from 'pinia'
import { billingClient } from '@/api/billing'
import type { Invoice, PaymentRequest } from '@/types/billing'

export const useBillingStore = defineStore('billing', {
  state: () => ({
    invoices: [] as Invoice[],
    currentInvoice: null as Invoice | null
  }),

  actions: {
    async getInvoice(id: string): Promise<Invoice> {
      const invoice = await billingClient.getInvoice(id)
      this.currentInvoice = invoice
      return invoice
    },

    async payInvoice(id: string): Promise<void> {
      await billingClient.payInvoice(id)
      // Refresh invoice
      await this.getInvoice(id)
    }
  }
})
```

### API Client Generation

```typescript
// Generated from IBillingService contract
import axios from 'axios'
import type { Invoice, PaymentRequest } from '@/types/billing'

const baseUrl = import.meta.env.VITE_BILLING_API_URL

export const billingClient = {
  async getInvoice(id: string): Promise<Invoice> {
    const response = await axios.get(`${baseUrl}/invoices/${id}`)
    return response.data
  },

  async payInvoice(id: string): Promise<void> {
    await axios.post(`${baseUrl}/invoices/${id}/pay`)
  }
}
```

## Angular Projections

### Component Generation

```typescript
// billing-invoice.component.ts
import { Component, OnInit, Input } from '@angular/core'
import { BillingService } from '../services/billing.service'
import { Invoice } from '../models/invoice'

@Component({
  selector: 'app-billing-invoice',
  templateUrl: './billing-invoice.component.html',
  styleUrls: ['./billing-invoice.component.css']
})
export class BillingInvoiceComponent implements OnInit {
  @Input() invoiceId!: string

  invoice: Invoice | null = null
  loading = false
  error: string | null = null

  constructor(private billingService: BillingService) {}

  ngOnInit(): void {
    this.loadInvoice()
  }

  async loadInvoice(): Promise<void> {
    this.loading = true
    try {
      this.invoice = await this.billingService.getInvoice(this.invoiceId)
    } catch (e) {
      this.error = e.message
    } finally {
      this.loading = false
    }
  }

  async payInvoice(): Promise<void> {
    await this.billingService.payInvoice(this.invoiceId)
    await this.loadInvoice()
  }
}
```

### Service Generation

```typescript
// billing.service.ts
import { Injectable } from '@angular/core'
import { HttpClient } from '@angular/common/http'
import { firstValueFrom } from 'rxjs'
import { Invoice, PaymentRequest } from '../models/billing'
import { environment } from '../../environments/environment'

@Injectable({
  providedIn: 'root'
})
export class BillingService {
  private baseUrl = environment.billingApiUrl

  constructor(private http: HttpClient) {}

  async getInvoice(id: string): Promise<Invoice> {
    return firstValueFrom(
      this.http.get<Invoice>(`${this.baseUrl}/invoices/${id}`)
    )
  }

  async payInvoice(id: string): Promise<void> {
    await firstValueFrom(
      this.http.post<void>(`${this.baseUrl}/invoices/${id}/pay`, {})
    )
  }
}
```

## MAUI Projections

### Page Generation

```xml
<!-- BillingInvoicePage.xaml -->
<?xml version="1.0" encoding="utf-8" ?>
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="BillingApp.Pages.BillingInvoicePage"
             Title="Invoice">
    <StackLayout Padding="20">
        <Label Text="Invoice Details" FontSize="24" FontAttributes="Bold" />

        <ActivityIndicator IsRunning="{Binding IsLoading}" IsVisible="{Binding IsLoading}" />

        <Label Text="{Binding ErrorMessage}"
               IsVisible="{Binding HasError}"
               TextColor="Red" />

        <StackLayout IsVisible="{Binding HasInvoice}">
            <Label Text="{Binding Invoice.InvoiceNumber}" FontSize="18" />
            <Label Text="{Binding Invoice.Amount, StringFormat='Amount: {0:C}'}" />
            <Label Text="{Binding Invoice.DueDate, StringFormat='Due: {0:d}'}" />

            <Button Text="Pay Invoice"
                    Command="{Binding PayInvoiceCommand}"
                    IsEnabled="{Binding CanPay}" />
        </StackLayout>
    </StackLayout>
</ContentPage>
```

### ViewModel Generation

```csharp
// BillingInvoiceViewModel.cs
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Billing.Contracts;

public partial class BillingInvoiceViewModel : ObservableObject
{
    private readonly IBillingService _billingService;

    [ObservableProperty]
    private Invoice? _invoice;

    [ObservableProperty]
    private bool _isLoading;

    [ObservableProperty]
    private string? _errorMessage;

    public bool HasInvoice => Invoice is not null;
    public bool HasError => !string.IsNullOrEmpty(ErrorMessage);
    public bool CanPay => Invoice is not null && !IsLoading;

    public BillingInvoiceViewModel(IBillingService billingService)
    {
        _billingService = billingService;
    }

    [RelayCommand]
    private async Task LoadInvoiceAsync(string invoiceId)
    {
        IsLoading = true;
        ErrorMessage = null;

        try
        {
            Invoice = await _billingService.GetInvoiceAsync(invoiceId);
        }
        catch (Exception ex)
        {
            ErrorMessage = ex.Message;
        }
        finally
        {
            IsLoading = false;
        }
    }

    [RelayCommand]
    private async Task PayInvoiceAsync()
    {
        if (Invoice is null) return;

        await _billingService.PayInvoiceAsync(Invoice.Id);
        await LoadInvoiceAsync(Invoice.Id);
    }
}
```

## WPF Projections

### View Generation

```xml
<!-- BillingInvoiceView.xaml -->
<UserControl x:Class="BillingApp.Views.BillingInvoiceView"
             xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <Grid Margin="20">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
        </Grid.RowDefinitions>

        <TextBlock Text="Invoice Details" FontSize="24" FontWeight="Bold" />

        <StackPanel Grid.Row="1" Margin="0,20,0,0">
            <ProgressBar IsIndeterminate="True"
                         Visibility="{Binding IsLoading, Converter={StaticResource BoolToVisibility}}" />

            <TextBlock Text="{Binding ErrorMessage}"
                       Foreground="Red"
                       Visibility="{Binding HasError, Converter={StaticResource BoolToVisibility}}" />

            <StackPanel Visibility="{Binding HasInvoice, Converter={StaticResource BoolToVisibility}}">
                <TextBlock Text="{Binding Invoice.InvoiceNumber}" FontSize="18" />
                <TextBlock Text="{Binding Invoice.Amount, StringFormat='Amount: {0:C}'}" />
                <TextBlock Text="{Binding Invoice.DueDate, StringFormat='Due: {0:d}'}" />

                <Button Content="Pay Invoice"
                        Command="{Binding PayInvoiceCommand}"
                        IsEnabled="{Binding CanPay}"
                        Margin="0,10,0,0" />
            </StackPanel>
        </StackPanel>
    </Grid>
</UserControl>
```

## Type Generation

All projections share generated TypeScript/C# types from the contract:

```typescript
// Generated from Invoice DTO
export interface Invoice {
  id: string
  invoiceNumber: string
  amount: number
  dueDate: Date
  status: InvoiceStatus
}

export enum InvoiceStatus {
  Pending = 'Pending',
  Paid = 'Paid',
  Overdue = 'Overdue'
}
```

## Generator Implementation

```csharp
public static string GenerateVueComponent(ContractInterface contract)
{
    var componentName = $"{contract.Name.TrimStart('I')}View";
    var props = contract.Methods.First().Parameters;
    var storeName = $"use{contract.Name.TrimStart('I')}Store";

    return $$"""
        <template>
          <div class="{{ToKebabCase(componentName)}}">
            <!-- Generated component structure -->
          </div>
        </template>

        <script setup lang="ts">
        import { ref, onMounted } from 'vue'
        import { {{storeName}} } from '@/stores/{{ToKebabCase(contract.Name)}}'

        // Generated component logic
        </script>
        """;
}
```

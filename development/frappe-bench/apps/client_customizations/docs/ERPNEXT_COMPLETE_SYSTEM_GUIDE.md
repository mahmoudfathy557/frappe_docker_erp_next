# ERPNext Complete System Guide & Reference Notebook
**Created**: 2026-07-18  
**Source**: https://frappe.io/erpnext/erp-guide  
**Version**: ERPNext Latest  
**Status**: Reference & Learning Notebook

---

## Table of Contents

1. [Overview](#overview)
2. [Part 1: Understanding ERPs](#part-1-understanding-erps)
3. [Part 2: Implementation & Configuration](#part-2-implementation--configuration)
4. [Part 3: Core Modules Deep-Dive](#part-3-core-modules-deep-dive)
5. [Part 4: Frontend Integration & Local Setup](#part-4-frontend-integration--local-setup)
6. [Quick Reference Index](#quick-reference-index)
7. [Resources & Links](#resources--links)

---

## Overview

This notebook serves as a comprehensive guide to ERPNext, the world's leading open-source Enterprise Resource Planning (ERP) system. It consolidates knowledge from the official ERPNext ERP Guide across all modules and provides practical frameworks for understanding business processes.

**Key Objectives:**
- Master 10 core ERPNext modules
- Understand inter-module integration patterns
- Reference module workflows and key transactions
- Compare ERPNext frontend with local Docker deployment
- Serve as a living document for team reference

---

# Part 1: Understanding ERPs

## 1.1 What is ERP?

An **Enterprise Resource Planning (ERP)** system is integrated software that consolidates business data and processes from across your organization into a single unified system.

**Key Characteristics:**
- **Centralized Data**: Single source of truth for all business information
- **Modular Design**: Distinct modules for different business functions
- **Integration**: Modules work together, sharing data seamlessly
- **Real-time Information**: Live dashboards and reports across departments
- **Scalability**: Grows with your business needs

**See Official Guide**: [The Importance of Business Sustainability](https://erpnext.com/erp-guide/business-sustainability)

## 1.2 Why Use ERP?

### Problems Solved by ERP:
1. **Data Silos**: Multiple spreadsheets and systems eliminated
2. **Manual Entry Errors**: Automation reduces mistakes
3. **Lack of Visibility**: Real-time insights across departments
4. **Inefficient Workflows**: Standardized, repeatable processes
5. **Compliance Issues**: Audit trails and proper documentation
6. **Cash Flow Uncertainty**: Integrated financial tracking

### Business Benefits:
- Improved efficiency and productivity
- Better decision-making with real-time data
- Reduced operational costs
- Enhanced customer relationships
- Regulatory compliance
- Scalability for growth

**See Official Guide**: [Why Use ERP and What is It?](https://erpnext.com/erp-guide/why-and-what-erp)

## 1.3 ERP Evaluation Criteria

Before implementing an ERP, evaluate based on:

1. **Functionality**: Does it cover all your business processes?
2. **Scalability**: Can it grow with your business?
3. **Customization**: Can it adapt to your unique processes?
4. **Cost**: Implementation and maintenance ROI
5. **Support**: Community and commercial support availability
6. **Integration**: APIs and third-party integrations
7. **Security**: Data protection and compliance
8. **Usability**: Ease of use for employees

**See Official Guide**: [Evaluating an ERP](https://erpnext.com/erp-guide/evaluating-an-erp)

---

# Part 2: Implementation & Configuration

## 2.1 Implementation Approaches

### Waterfall Method
- Traditional phased approach
- Upfront complete configuration
- Longer implementation timeline
- Higher upfront costs

### Agile Implementation Method ✓ Recommended
- Iterative, sprint-based approach
- Continuous feedback and adjustment
- Faster value realization
- Lower risk through staged rollout
- Better stakeholder engagement

**See Official Guide**: [Implementing an ERP Software](https://erpnext.com/erp-guide/implementing-an-erp)  
**See Official Guide**: [Constructing an Agile Implementation Plan](https://erpnext.com/erp-guide/constructing-agile-implementation-plan)

## 2.2 Understanding Current System

### Gap Analysis Framework:
1. **As-Is Assessment**: Document current state
   - Current tools and systems
   - Manual processes
   - Pain points and inefficiencies
   - Data structure and flow

2. **To-Be Vision**: Define desired state
   - Target processes
   - Automation opportunities
   - Integration points
   - Success metrics

3. **Gap Identification**: What needs to change
   - Process changes
   - Configuration requirements
   - Custom development needs
   - Training requirements

**See Official Guide**: [Understanding the Current System](https://erpnext.com/erp-guide/understanding-current-system)

## 2.3 ERP Configuration Essentials

### Critical Configuration Areas:

#### **Company Setup**
- Legal entity information
- Financial book setup
- Default settings
- Currency configuration
- Tax registration details

#### **Chart of Accounts**
- Account structure
- Account types (Asset, Liability, Equity, Income, Expense)
- Hierarchical organization
- Double-entry accounting foundation

#### **Fiscal Year & Periods**
- Financial year boundaries
- Accounting periods (monthly, quarterly)
- Opening/closing procedures
- Year-end processes

#### **Cost Centers**
- Organizational cost allocation
- Department mapping
- Budget allocation
- Distributed cost center logic

#### **Warehouse & Locations**
- Physical storage locations
- Virtual warehouses for organization
- Default warehouse assignment
- Location-based processes

#### **Master Data**
- Customers, suppliers, employees
- Items/products
- Salesperson assignments
- Territory mapping

**See Official Guide**: [Configuring Your ERP System](https://erpnext.com/erp-guide/configuring-your-erp-system)

---

# Part 3: Core Modules Deep-Dive

## 3.1 CRM Module - Customer Relationship Management

**Purpose**: Manage presales activities, lead tracking, and customer relationships

**Official Guide**: [Customer Relationship Management (CRM)](https://erpnext.com/erp-guide/crm-system)

### Module Overview

| Aspect | Details |
|--------|---------|
| **Primary Focus** | Presales process, lead capture, opportunity tracking |
| **Key Users** | Sales managers, salespersons, marketing |
| **Integration** | Feeds into Sales module |
| **Core Value** | Centralized customer intelligence, relationship tracking |

### Key Entities & Transactions

#### **Leads**
- **Definition**: Potential customers (pre-existing or cold)
- **Key Fields**: Name, source, contact info, qualification status
- **Purpose**: Capture and qualify prospects
- **Workflow**: Lead → Opportunity → Customer

#### **Lead Source**
- **Definition**: Channel through which leads are generated
- **Examples**: Website, referral, cold call, event, advertisement
- **Value**: Measure marketing campaign effectiveness

#### **Opportunities**
- **Definition**: Qualified leads showing buying signals
- **Statuses**: Open, Won, Lost, Converted
- **Key Fields**: Amount, probability, sales stage, expected close date
- **Purpose**: Track sales pipeline and forecast revenue

#### **Opportunity Type**
- **Categories**: Sales, Support, Maintenance, Partnership
- **Value**: Route opportunities to appropriate sales resources

#### **Sales Stage**
- **Definition**: Position in sales cycle (Prospect, Negotiation, Proposal, etc.)
- **Value**: Visibility into pipeline stage distribution

#### **Customer Group**
- **Definition**: Segmentation of customers by characteristics
- **Examples**: Enterprise, SMB, Retail, Wholesale
- **Value**: Target groups with specific pricing, campaigns

#### **Campaigns**
- **Definition**: Marketing initiatives to generate leads
- **Functions**: Track leads generated, schedule emails, social media posts
- **Value**: Measure campaign ROI

#### **Newsletter**
- **Definition**: Periodic informational communications
- **Purpose**: Customer engagement, soft sales push
- **Features**: Subscriber management, scheduling

### CRM Workflow Setup

```
1. Lead Capture & Import
   ↓
2. Lead Assignment to Salespersons
   ↓
3. Lead Qualification & Follow-up
   ↓
4. Opportunity Creation
   ↓
5. Sales Stage Tracking
   ↓
6. Win/Loss Analysis
   ↓
7. Campaign Effectiveness Reporting
```

### Key Reports

| Report | Purpose |
|--------|---------|
| Lead Details | Comprehensive lead information and status |
| Sales Funnel | Prospects at each stage, conversion rates |
| Opportunity Pipeline | Open opportunities by salesperson/stage |
| Campaign Performance | Leads generated vs. campaign investment |

### CRM Benefits

✓ Centralized customer data  
✓ Transparent sales pipeline  
✓ Improved lead follow-up  
✓ Data-driven sales forecasting  
✓ Better resource allocation  

---

## 3.2 Sales Module - Selling / Sales Order Management

**Purpose**: Manage customer quotes, sales orders, and delivery process

**Official Guide**: [Sales System](https://erpnext.com/erp-guide/sales-system)

### Module Overview

| Aspect | Details |
|--------|---------|
| **Primary Focus** | Active selling process from quote to delivery |
| **Key Users** | Sales executives, delivery team, sales managers |
| **Integration** | Connected to CRM (upstream), Inventory & Accounting (downstream) |
| **Core Value** | Order tracking, delivery management, revenue recognition |

### Key Entities & Transactions

#### **Customer**
- **Definition**: Entity purchasing goods/services from your business
- **Master Data**: Tax ID, billing address, credit limit, price list
- **Purpose**: Maintain customer database and settings

#### **Quotation (Proposal)**
- **Definition**: Estimated pricing and terms for potential sale
- **Components**: Item list, pricing, taxes, T&C, validity period
- **Status**: Draft → Submitted
- **Conversion**: Can be converted to Sales Order

#### **Sales Order**
- **Definition**: Binding agreement between seller and buyer
- **Status Flow**: Draft → Submitted → Partially Delivered → Delivered → Closed
- **Key Fields**: Customer, items, quantities, pricing, delivery date
- **Integration Point**: Creates Delivery Notes when items ship

#### **Blanket Order**
- **Definition**: Long-term agreement for periodic supply at fixed rate
- **Use Case**: Recurring orders for standard items
- **Workflow**: Generates Sales Orders based on delivery schedule

#### **Sales Partner**
- **Definition**: Channel partner (distributor, agent, reseller)
- **Commission**: Auto-calculated based on transaction amount
- **Types**: Dealer, distributor, agent, retailer, reseller
- **Purpose**: Track partner contributions and commissions

#### **Salesperson**
- **Definition**: Employee responsible for selling
- **Settings**: Territory assignment, sales targets
- **Tracking**: Commission calculations, performance metrics

### Sales Workflow

```
1. Customer Created in System
   ↓
2. Opportunity (from CRM) → Sales Order Created
   ↓
3. Quotation Sent to Customer
   ↓
4. Quotation Approved → Sales Order Created
   ↓
5. Sales Order Confirmed & Submitted
   ↓
6. Inventory Allocated for Delivery
   ↓
7. Delivery Note Created
   ↓
8. Sales Invoice Generated & Delivered
   ↓
9. Payment Received (Accounting Module)
```

### Key Reports

| Report | Purpose |
|--------|---------|
| Sales Analytics | Sales performance analysis by customer, item, territory |
| Sales Order Analysis | Current billing and delivery status |
| Sales Order Trends | Sales patterns over time periods |
| Outstanding Orders | Pending deliveries and billing |

### Sales Benefits

✓ Structured sales pipeline  
✓ Real-time order tracking  
✓ Inventory visibility linked to orders  
✓ Automated invoice generation  
✓ Commission management  
✓ Multi-channel sales support  

---

## 3.3 Procurement Module - Buying / Purchase Orders

**Purpose**: Manage supplier relationships, purchase requests, and procurement process

**Official Guide**: [Procurement System](https://erpnext.com/erp-guide/procurement-system)

### Module Overview

| Aspect | Details |
|--------|---------|
| **Primary Focus** | Purchase lifecycle from request to receipt |
| **Key Users** | Procurement managers, inventory team, approvers |
| **Integration** | Feeds inventory, impacts accounting via expenses |
| **Core Value** | Cost control, supplier management, inventory replenishment |

### Key Entities & Transactions

#### **Item**
- **Definition**: Any product, material, or service purchased
- **Categories**: Raw material, finished goods, service, asset
- **Attributes**: Code, UOM, supplier, lead time
- **Purpose**: Master catalog of purchasable items

#### **Supplier**
- **Definition**: Vendor providing goods/services to your business
- **Master Data**: Contact, payment terms, rating, price list
- **Scorecard**: Quality, delivery, responsiveness tracking
- **Purpose**: Centralize vendor management

#### **Material Request (Purchase)**
- **Definition**: Internal request to purchase materials
- **Status Flow**: Draft → Submitted → Ordered
- **Trigger**: Inventory planning, work order, sales order
- **Purpose**: Approve purchases before vendor selection

#### **Request for Quotation (RFQ)**
- **Definition**: Formal document requesting pricing from suppliers
- **Process**: Sent after Material Request approval
- **Response**: Suppliers respond with Supplier Quotations
- **Purpose**: Compare options before purchase decision

#### **Supplier Quotation**
- **Definition**: Vendor's offer for items with terms and pricing
- **Response**: Received in response to RFQ
- **Evaluation**: Compare cost, quality, delivery time
- **Conversion**: Selected quotation converts to Purchase Order

#### **Purchase Order (PO)**
- **Definition**: Binding contract with supplier
- **Status Flow**: Draft → Submitted → Partially Received → Received → Closed
- **Key Fields**: Supplier, items, quantities, pricing, payment terms, delivery date
- **Importance**: Creates binding obligation, triggers payment tracking

### Purchasing Workflow

```
1. Material Requirement Identified
   ↓
2. Material Request Created & Approved
   ↓
3. Request for Quotation (RFQ) Sent to Suppliers
   ↓
4. Supplier Quotations Received & Evaluated
   ↓
5. Best Quotation Selected
   ↓
6. Purchase Order (PO) Created & Submitted
   ↓
7. Supplier Ships Items
   ↓
8. Purchase Receipt Created (inventory updated)
   ↓
9. Purchase Invoice Received (payment tracked)
   ↓
10. Payment Processed (Accounting Module)
```

### Key Reports

| Report | Purpose |
|--------|---------|
| Purchase Analytics | Spending analysis by supplier, item, category |
| Purchase Order Analysis | Item billing status in POs |
| Purchase Order Trends | Purchasing patterns over time |
| Supplier Performance | Supplier quality, delivery, responsiveness |
| Purchase Trends | Cost trends and optimization opportunities |

### Procurement Benefits

✓ Cost control through quotation comparison  
✓ Centralized supplier management  
✓ Approval workflows prevent unauthorized spending  
✓ Visibility into supplier performance  
✓ Automatic inventory updates  
✓ Audit trail for compliance  

---

## 3.4 Accounting Module - Financial Management

**Purpose**: Manage all financial transactions, reporting, and compliance

**Official Guide**: [Accounting System](https://erpnext.com/erp-guide/accounting-system)

### Module Overview

| Aspect | Details |
|--------|---------|
| **Primary Focus** | Double-entry accounting, financial statements, tax compliance |
| **Key Users** | Accountants, CFO, finance managers, tax consultants |
| **Integration** | Center of integration - receives data from all modules |
| **Core Value** | Financial accuracy, compliance, decision-making data |

### Foundational Concepts

#### **Chart of Accounts (CoA)**
- **Definition**: Complete list of all accounts used in accounting
- **Structure**: Hierarchical organization of accounts
- **Account Types**: 
  - **Balance Sheet**: Assets, Liabilities, Equity
  - **P&L**: Income, Expenses
- **Double-Entry**: Every transaction affects at least 2 accounts
- **Purpose**: Blueprint for consistent financial recording

#### **Company Setup**
- **Definition**: Master configuration for legal entity
- **Includes**: Company name, currency, fiscal year, tax settings, defaults
- **Scope**: All transactions must reference a company
- **Purpose**: Multi-company support and isolation

#### **Fiscal Year**
- **Definition**: Accounting period (typically 12 months)
- **Varies by**: Country, jurisdiction, company preference
- **Examples**: Calendar year (Jan-Dec), April year (Apr-Mar)
- **Purpose**: Organize financial reporting periods

#### **Accounting Period**
- **Definition**: Sub-period within fiscal year (monthly, quarterly)
- **Purpose**: Regular financial statement generation
- **Controls**: Can restrict posting outside open periods

#### **Cost Center**
- **Definition**: Organizational division for cost/income allocation
- **Examples**: Department, project, business unit
- **Features**: Can distribute costs across multiple centers
- **Purpose**: Department-level profitability tracking

#### **Opening Balance**
- **Definition**: Starting balances when switching accounting systems
- **Components**: Assets and liabilities from previous system
- **Importance**: Critical for accurate financial statements
- **Timing**: Entered at implementation start date

### Key Transactions

#### **Sales Invoice**
- **Definition**: Bill sent to customer for goods/services provided
- **Trigger**: Created from Delivery Note or Sales Order
- **Status**: Draft → Submitted → Partially Paid → Paid
- **Impact**: Records revenue, creates receivable

#### **Purchase Invoice**
- **Definition**: Bill received from supplier for purchase
- **Trigger**: Created from Purchase Receipt
- **Status**: Draft → Submitted → Partially Paid → Paid
- **Impact**: Records expense, creates payable

#### **Journal Entry**
- **Definition**: Manual accounting entry for transactions not covered by other docs
- **Use Cases**: Adjustments, payments, transfers, accruals
- **Structure**: Debit/credit pairs that balance
- **Purpose**: Handle complex or non-standard transactions

#### **Credit Note**
- **Definition**: Credit issued to customer for return of goods/services
- **Created Against**: Sales Invoice
- **Amount**: Less than or equal to original invoice
- **Purpose**: Manage returns and allowances

#### **Debit Note**
- **Definition**: Debit issued to supplier for return of goods/services
- **Created Against**: Purchase Invoice
- **Purpose**: Manage supplier returns

### Accounting Module Components

#### **Banking**
- **Bank Accounts**: Record company and supplier/customer accounts
- **Bank Reconciliation**: Match ERP records with actual bank statements
- **Purpose**: Ensure cash accuracy

#### **Tax Management**
- **Tax Rules**: Configure tax calculations by criteria
- **Tax Categories**: Different tax treatments for different item types
- **Tax Withholding**: TDS (Tax Deducted at Source) configurations
- **VAT/GST**: Multi-stage value-added tax support
- **Item Tax Templates**: Override standard tax rates for specific items
- **Purpose**: Automate tax compliance

#### **Share Management**
- **Shareholders**: Record company ownership
- **Share Transfers**: Track changes in share structure
- **Share Ledger**: Complete transaction history
- **Purpose**: Equity tracking and compliance

### Key Financial Reports

| Report | Purpose |
|--------|---------|
| General Ledger | Complete transaction detail for all accounts |
| Trial Balance | Verify accounts balance (debits = credits) |
| Balance Sheet | Assets, Liabilities, Equity snapshot at point in time |
| Profit & Loss Statement | Revenue, expenses, net income for period |
| Cash Flow Statement | Money movement analysis |
| Accounts Receivable (AR) | Outstanding customer amounts with aging |
| Accounts Payable (AP) | Outstanding supplier amounts with aging |
| Sales & Purchase Register | Sales/purchase transactions with tax detail |

### Accounting Benefits

✓ Accurate financial records with double-entry system  
✓ Real-time financial statements  
✓ Tax compliance and audit trails  
✓ Multi-company support  
✓ Integrated with all business modules  
✓ Reduced manual data entry errors  

---

## 3.5 Inventory Module - Stock Management

**Purpose**: Manage inventory levels, stock movements, and warehouse operations

**Official Guide**: [Inventory Management](https://erpnext.com/erp-guide/inventory-management)

### Module Overview

| Aspect | Details |
|--------|---------|
| **Primary Focus** | Stock level management, warehouse operations, material movement |
| **Key Users** | Warehouse staff, inventory managers, procurement |
| **Integration** | Supplies manufacturing, fulfills sales, impacts accounting |
| **Core Value** | Prevents stockouts, reduces holding costs, accurate valuation |

### Key Entities

#### **Warehouse**
- **Definition**: Physical or virtual storage location
- **Types**: Physical warehouses, virtual staging areas, reject warehouses
- **Default Assignment**: Items assigned to default warehouses
- **Purpose**: Location-based inventory tracking and movement

#### **Item**
- **Definition**: Product, material, or service tracked in inventory
- **Key Fields**: Item code, UOM, category, supplier, reorder level
- **Attributes**: Serial number, batch, expiry date, weight
- **Purpose**: Master catalog for supply chain

#### **Stock Entry**
- **Definition**: Internal document recording item movement
- **Types**:
  - **Material Transfer**: Move between warehouses
  - **Material Issue**: Remove from stock (manufacturing, consumption)
  - **Material Receipt**: Add to stock
  - **Stock Adjustment**: Reconcile counted stock
- **Purpose**: Record all internal stock movements

### Core Transactions

#### **Purchase Receipt**
- **Definition**: Accept items from supplier against Purchase Order
- **Status**: Draft → Submitted (creates Stock Ledger Entry)
- **Process**:
  1. Receive items
  2. Quality inspection (if required)
  3. Record serial/batch numbers
  4. Submit receipt
- **Impact**: Updates inventory quantity and value
- **Integration**: Updates PO status, creates Stock Ledger

#### **Delivery Note**
- **Definition**: Shipment document when items leave warehouse
- **Status**: Draft → Submitted → Invoiced
- **Created From**: Sales Order
- **Process**:
  1. Pick items from warehouse
  2. Record serial/batch numbers
  3. Submit delivery
  4. Generates Sales Invoice
- **Impact**: Reduces inventory, triggers invoicing

#### **Quality Inspection**
- **Definition**: QA check before/after item transaction
- **Trigger**: Can be mandatory for specified items
- **Parameters**: Sample size, inspection criteria, accept/reject
- **Purpose**: Ensure quality standards

### Advanced Features

#### **Serialization**
- **Definition**: Assign unique serial number to each item
- **Tracks**: Location, warranty, expiry, recalls
- **Benefit**: Individual item tracking for high-value items
- **Examples**: Laptops, machinery, electronics

#### **Batch/Lot Tracking**
- **Definition**: Group items produced together
- **Useful For**: Expiry tracking, recalls, returns tracing
- **Combined With**: Serialization for comprehensive tracking
- **Examples**: Pharmaceuticals, food, beverages

#### **Stock Reconciliation**
- **Definition**: Adjust ERP inventory to match physical count
- **When Used**: Implementation (Opening Stock), periodic audits
- **Process**: Count physical items, adjust ERP to match
- **Purpose**: Correct discrepancies between physical and system

### Stock Movement Workflow

```
1. Purchase Order Created
   ↓
2. Goods Arrive
   ↓
3. Purchase Receipt Created
   ↓
4. Quality Inspection (if required)
   ↓
5. Stock Added to Warehouse (Stock Ledger Entry)
   ↓
6. Sales Order Created
   ↓
7. Inventory Allocated to Order
   ↓
8. Delivery Note Created
   ↓
9. Stock Deducted from Warehouse
   ↓
10. Sales Invoice Generated
```

### Key Reports

| Report | Purpose |
|--------|---------|
| Stock Ledger | Complete history of stock movements |
| Stock Balance | Current quantity in each warehouse |
| Stock Projected Quantity | Current + pending + ordered - reserved |
| Stock Valuation | Current inventory value |
| Expiring Items | Items approaching expiry date |
| Batch-wise Balance | Balance for specific batch |
| Warehouse-wise Stock | Distribution across locations |

### Projected Quantity Components

```
Projected Qty = Actual Qty 
              + Ordered Qty (from PO)
              + Planned Qty (from Work Order)
              + Indented Qty (from Material Request)
              - Reserved Qty (from Sales Order)
              - Reserved for Production
              - Reserved for Subcontract
```

### Inventory Benefits

✓ Real-time stock visibility  
✓ Prevents stockouts and overstocking  
✓ Accurate inventory valuation  
✓ Waste reduction through expiry/batch tracking  
✓ Location-based organization  
✓ Integrated with sales and procurement  

---

## 3.6 Manufacturing Module - Production Management

**Purpose**: Manage production processes, work orders, and bill of materials

**Official Guide**: [Manufacturing](https://erpnext.com/erp-guide/manufacturing)

### Module Overview

| Aspect | Details |
|--------|---------|
| **Primary Focus** | Production planning, work order execution, BOM management |
| **Key Users** | Production managers, shop floor supervisors, planners |
| **Integration** | Consumes inventory, creates inventory, employs resources |
| **Core Value** | Efficient production, quality control, resource optimization |

### Manufacturing Types Supported

1. **Discrete**: Individual items from parts (typical manufacturing)
2. **Make-to-Order**: Manufacture after customer order
3. **Make-to-Stock**: Bulk production based on demand forecast
4. **Engineer-to-Order**: Custom design then manufacture
5. **Repetitive**: Dedicated production line for same item
6. **Process**: Continuous process (chemicals, beverages, pharmaceuticals)
7. **Batch**: Periodic production in batches

### Key Entities

#### **Item**
- **Definition**: Any purchasable, saleable, or manufacturable product
- **Scope**: Raw materials, sub-assemblies, finished goods, services
- **Master Data**: Item code, UOM, category, manufacturing settings
- **Purpose**: Catalog of everything in supply chain

#### **Bill of Materials (BOM)**
- **Definition**: List of items (components) and operations needed to produce another item
- **Core Components**: Materials (with quantities), Operations, Workstations
- **Importance**: Heart of manufacturing system
- **Purpose**: Defines how products are made
- **Example**: Laptop BOM includes CPU, RAM, HDD, motherboard, assembly operations

#### **Multi-Level BOM**
- **Definition**: BOMs containing sub-assemblies that have their own BOMs
- **Use Case**: Complex products needing intermediate assembly
- **Example**:
  - Laptop (top level)
    - Module A (sub-assembly with own BOM)
      - Component 1, Component 2
    - Module B (sub-assembly with own BOM)
      - Component 3, Component 4

#### **Operation**
- **Definition**: Manufacturing process/step applied to materials
- **Examples**: Dyeing, cutting, assembly, welding, inspection
- **Attributes**: Operation description, standard time, cost
- **Purpose**: Define production activities

#### **Workstation**
- **Definition**: Physical location where operations are performed
- **Master Data**: Cost per hour, production capacity, working hours
- **Efficiency Settings**: Cycle time, buffer time
- **Purpose**: Resource allocation and scheduling

#### **Work Order**
- **Definition**: Production authorization document
- **Triggers**: Sales Orders, Material Requests, Production Plan
- **Components**: Item to produce, quantity, BOM reference, deadline
- **Process**: Generates Material Requirements & Job Cards
- **Status Flow**: Draft → Submitted → In Progress → Completed → Closed
- **Impact**: Allocates inventory for production

#### **Job Card**
- **Definition**: Shop floor document for specific operation at workstation
- **Created From**: Work Order
- **Assignment**: Assigned to workstations
- **Data**: Material to use, operations, time tracking, quality checks
- **Purpose**: Guide production operators

#### **Material Request**
- **Definition**: Request for materials (different types)
- **Types**:
  - **Purchase**: Request to buy from external supplier
  - **Material Transfer**: Request to move between warehouses
  - **Material Issue**: Request to issue for manufacturing
  - **Manufacture**: Request to produce internally
- **Purpose**: Central mechanism to request anything

### Production Planning

#### **Production Planning Tool**
- **Purpose**: Plan production and purchases for future period
- **Input**: Sales Orders, demand forecasts, inventory levels
- **Output**: Work Orders (for manufacturing), Purchase Orders (for buying)
- **Logic**: Considers lead times, safety stock, batch sizes
- **Benefit**: Coordinate production and procurement

### Manufacturing Workflow

```
1. Sales Order Created or Material Demand Identified
   ↓
2. Work Order Created for Required Item
   ↓
3. Work Order Generates Material Requirements (Stock Entries)
   ↓
4. Required Materials Issued to Shop Floor (Stock Entry)
   ↓
5. Job Cards Created for Each Operation
   ↓
6. Production Occurs at Workstations
   ↓
7. Quality Inspection at Each Stage
   ↓
8. Work Order Marked Complete
   ↓
9. Finished Goods Added Back to Inventory
   ↓
10. Delivery to Customer (via Delivery Note)
```

### Key Reports

| Report | Purpose |
|--------|---------|
| Work Order Summary | Current status of all production orders |
| Job Card Summary | Operation progress tracking |
| Production Analytics | Capacity utilization, productivity metrics |
| BOM Comparison | Track BOM versions and changes |
| Production Plan | Forecasted vs. actual production |

### Manufacturing Benefits

✓ Standardized production through BOMs  
✓ Real-time shop floor visibility  
✓ Optimized resource utilization  
✓ Quality control at each stage  
✓ Integrated material planning  
✓ Production cost tracking  

---

## 3.7 HRMS Module - Human Resources

**Purpose**: Manage employees, recruitment, payroll, and HR processes

**Official Guide**: [Human Resource Management](https://erpnext.com/erp-guide/human-resource-management)

### Module Overview

| Aspect | Details |
|--------|---------|
| **Primary Focus** | Employee lifecycle, payroll, recruitment, leave management |
| **Key Users** | HR managers, department heads, employees |
| **Integration** | Feeds expense and project modules, impacts accounting |
| **Core Value** | Compliance, employee satisfaction, cost management |

### Core Employee Management

#### **Employee**
- **Master Data**: 
  - Personal: Name, date of birth, address, contact
  - Professional: Department, designation, employment type, branch
  - Financial: Salary, bank account, tax information
  - Benefits: Health insurance details, leave allocations
- **Lifecycle**: Onboarding → Active → Transfer → Promotion → Separation
- **Purpose**: Central employee database

#### **Employment Types**
- Full-time, part-time, contractor, intern, temporary, probation
- Purpose: Configure benefits, leave, and payroll differently

### Recruitment Process

#### **Staffing Plan**
- **Definition**: Manpower requirement plan for period
- **Components**: Positions needed, estimated cost, headcount by department
- **Benefit**: Budget planning for recruitment

#### **Job Opening**
- **Definition**: Published vacancy for position
- **Details**: Job title, department, qualifications, salary range
- **Process**: Posted and applicants apply

#### **Job Applicant**
- **Definition**: Person who applies for job
- **Process**: Screening → Interview → Offer → Appointment
- **Tracking**: Interview rounds, feedback, decision

#### **Job Offer**
- **Definition**: Formal offer with terms (salary, position, start date)
- **Includes**: Salary, designation, joining date, leave entitlement

#### **Appointment Letter**
- **Definition**: Final employment authorization
- **Created After**: Job Offer acceptance
- **Purpose**: Legal documentation of employment

### Leave Management

#### **Leave Type**
- **Definition**: Classification of leave (Casual, Sick, Earned, Unpaid, etc.)
- **Rules**: Max days, carry forward, continuous days allowed
- **Features**: Holidays included in leave, optional leave, compensatory

#### **Leave Allocation**
- **Definition**: Number of leave days allocated to employee for period
- **Based On**: Leave policy, employee tenure, leave type
- **Example**: 20 casual days per year

#### **Leave Application**
- **Definition**: Employee request to take leave
- **Status**: Draft → Submitted → Approved → Rejected
- **Process**: Submit → Approval → Adjustment → Accounting
- **Impact**: Reduces allocated balance, may affect salary

#### **Leave Ledger**
- **Definition**: Complete history of all leave transactions
- **Transactions**: Allocations, applications, encashments
- **Purpose**: Audit trail for compliance

#### **Holiday List**
- **Definition**: Dates when company is closed (national holidays, etc.)
- **Scope**: Can vary by location/department
- **Impact**: Affects leave calculations

#### **Leave Block List**
- **Definition**: Dates when employees cannot take leave
- **Examples**: Year-end closing, critical business period
- **Purpose**: Protect critical business periods

#### **Leave Encashment**
- **Definition**: Payment for unused accumulated leave
- **Amount**: Calculated based on salary rate and unused days
- **Compliance**: Follow legal regulations per jurisdiction

### Attendance & Shifts

#### **Attendance**
- **Definition**: Record of employee presence on given day
- **Status**: Present, Absent, Half Day, On Leave, Work From Home
- **Marking**: Manual entry or automatic via check-in system
- **Purpose**: Track attendance, link to payroll

#### **Shift**
- **Definition**: Time period during which employee works
- **Types**: Day shift, night shift, rotating shift
- **Purpose**: Support 24/7 operations with rotating staff

#### **Shift Request**
- **Definition**: Employee request for different shift
- **Process**: Submit → Approval → Assignment update
- **Purpose**: Manage shift preferences

#### **Employee Check-in**
- **Definition**: Time-based check-in for shift tracking
- **Automatic Attendance**: Can auto-mark attendance if checked in
- **Purpose**: Modern attendance tracking

### Employee Lifecycle

#### **Employee Onboarding**
- **Definition**: Process of integrating new employee
- **Tasks Generated**: Background check, email setup, equipment, training, policy acknowledgment
- **Purpose**: Smooth ramp-up for new hires

#### **Employee Appraisal**
- **Definition**: Performance evaluation
- **Components**: KRAs (Key Result Areas), goals, self-assessment, manager feedback
- **Purpose**: Performance management and development

#### **Employee Skill Map**
- **Definition**: Record of employee competencies and skill level
- **Used For**: Appraisals, project assignments, training needs
- **Purpose**: Skills inventory for organization

#### **Employee Promotion**
- **Definition**: Career advancement document
- **Updates**: Designation, salary, department (if applicable)
- **Purpose**: Document career progression

#### **Employee Transfer**
- **Definition**: Movement between departments or locations
- **Details**: New department, designation, location, effective date
- **Purpose**: Track organizational changes

#### **Employee Separation**
- **Definition**: Exit process when employee leaves
- **Tasks**: Collect company assets, clear dues, disable access, exit interview
- **Purpose**: Orderly offboarding

### Payroll Management

#### **Salary Structure**
- **Definition**: Template defining pay components
- **Components**:
  - **Earnings**: Base salary, allowances, bonuses, commissions
  - **Deductions**: Taxes, insurance, loans, other deductions
- **Used For**: Salary calculation, benefits administration
- **Purpose**: Consistent salary calculation

#### **Salary Component**
- **Definition**: Individual line item in salary
- **Types**: Fixed or variable
- **Formula**: Can have conditional logic
- **Examples**: HRA (House Rent Allowance), Provident Fund

#### **Salary Structure Assignment**
- **Definition**: Linking salary structure to employee
- **Effective Date**: When structure applies
- **Purpose**: Track salary changes over time

#### **Salary Slip**
- **Definition**: Monthly paycheck breakdown
- **Contents**: Earnings, deductions, net pay, tax calculations
- **Generated**: Via Payroll Entry (bulk) or manually
- **Purpose**: Employee paycheck record, tax documentation

#### **Payroll Entry**
- **Definition**: Bulk processing of salary slips
- **Scope**: Can be company-wide or by department/branch
- **Process**: Generate slips → Review → Submit → Create Journal Entry
- **Impact**: Books salary expense in accounting

#### **Additional Salary**
- **Definition**: Extra payment outside regular salary
- **Examples**: Bonus, one-time allowance, severance
- **Process**: Create, approve, include in next payroll
- **Purpose**: Handle non-standard payments

#### **Employee Benefit Application**
- **Definition**: Employee selection of flexible benefits
- **Timing**: Typically once per year
- **Scope**: Based on assigned salary structure
- **Purpose**: Personalize benefits package

### HR Reports

| Report | Purpose |
|--------|---------|
| Employee Leave Balance | Current leave balance per employee |
| Employee Holiday Attendance | Presence on holidays |
| Monthly Salary Register | All employee salaries for month |
| Vehicle Expenses | Fleet vehicle cost tracking |
| Loan Repayment | Tracking of employee loans |
| Bank Remittance | Salary payment file for bank |

### HRMS Benefits

✓ Centralized employee database  
✓ Automated payroll with tax compliance  
✓ Leave and attendance accuracy  
✓ Recruitment pipeline management  
✓ Performance tracking  
✓ Compliance documentation  

---

## 3.8 Asset Management Module

**Purpose**: Track and manage company assets throughout their lifecycle

**Official Guide**: [Asset Management](https://erpnext.com/erp-guide/asset-management)

### Module Overview

| Aspect | Details |
|--------|---------|
| **Primary Focus** | Fixed asset lifecycle, depreciation, maintenance |
| **Key Users** | Finance, facilities, maintenance team |
| **Integration** | Connected to accounting (depreciation), CRM (maintenance tasks) |
| **Core Value** | Maximize ROI on assets, reduce costs, compliance |

### Asset Classification

#### **By Convertibility**
- **Current Assets**: Easily converted to cash within year (inventory, receivables)
- **Fixed Assets**: Long-term, not easily converted (land, machinery, buildings)

#### **By Physical Existence**
- **Tangible Assets**: Physical items (vehicles, equipment, property)
- **Intangible Assets**: Non-physical (patents, copyrights, trademarks)

#### **By Usage**
- **Operating Assets**: Required for daily business (machinery, patents, cash)
- **Non-Operating Assets**: Generate revenue without daily use (investments, vacant land)

### Asset Lifecycle

#### **Asset Purchase**
- **Definition**: Acquisition of new asset
- **Process**:
  1. Create Purchase Order (from Procurement)
  2. Create Asset Master record
  3. Record purchase in Accounting
  4. Set depreciation parameters
- **Valuation**: Record at cost (purchase + shipping + installation)

#### **Asset Location**
- **Definition**: Current physical location of asset
- **Examples**: Office, warehouse, manufacturing plant, site
- **Purpose**: Track asset distribution

#### **Asset Movement**
- **Definition**: Movement from one location to another
- **Record**: Asset Movement document
- **Purpose**: Audit trail for asset location

#### **Asset Value Adjustment**
- **Definition**: Adjustment to asset value
- **Reasons**: Damage, obsolescence, market value changes
- **Impact**: Affects depreciation calculation and financial statements

#### **Asset Maintenance**
- **Definition**: Activities to maintain asset performance
- **Types**: Preventive, calibration, repair
- **Scheduling**: Based on start date and frequency
- **Logging**: Asset Maintenance Log tracks all activities
- **Purpose**: Extend asset life, maintain reliability

#### **Asset Repair**
- **Definition**: Restoration of broken asset
- **Record**: Failure date, description, repair cost, actions taken
- **Purpose**: Track repair history and costs

#### **Asset Depreciation**
- **Definition**: Gradual value loss over asset lifetime
- **Methods Supported**: Straight-line, declining balance, etc.
- **Schedule**: Automatically created based on parameters
- **Accounting**: Monthly depreciation entries
- **Purpose**: Spread cost over useful life

#### **Asset Scrapping/Disposal**
- **Definition**: Removal of asset from service
- **Sale**: Can record sales with gain/loss
- **Scrap**: Record as worthless
- **Accounting Impact**: Remove from asset account, record gain/loss
- **Purpose**: Complete asset lifecycle

### Asset Management Features

#### **Asset Category**
- **Definition**: Classification of similar assets
- **Examples**: Machinery, Vehicles, Office Equipment, Furniture
- **Purpose**: Group assets for reporting and policy

#### **Asset Maintenance Team**
- **Definition**: Employees responsible for maintenance
- **Assignment**: Linked to specific assets or asset categories
- **Tasks**: Auto-generated based on maintenance schedule
- **Purpose**: Assign responsibility for upkeep

### Key Reports

| Report | Purpose |
|--------|---------|
| Asset Depreciation Ledger | Purchase, depreciation, current value by asset |
| Fixed Asset Register | Complete details of all fixed assets |
| Asset Depreciation & Balances | Cost, depreciation, and net value by category |
| Asset Maintenance Schedule | Upcoming maintenance dates |

### Asset Benefits

✓ Complete asset visibility  
✓ Accurate depreciation for compliance  
✓ Maintenance tracking reduces costs  
✓ Audit trail for regulatory compliance  
✓ ROI maximization through proper maintenance  
✓ Integrated with accounting for financial accuracy  

---

## 3.9 Project Management Module

**Purpose**: Plan, execute, and monitor projects with task and resource management

**Official Guide**: [Project Management](https://erpnext.com/erp-guide/project-management)

### Module Overview

| Aspect | Details |
|--------|---------|
| **Primary Focus** | Project planning, task allocation, cost tracking, profitability |
| **Key Users** | Project managers, team leads, resource managers |
| **Integration** | Linked to sales (projects), purchases, timesheets (time tracking) |
| **Core Value** | On-time, on-budget project delivery, resource optimization |

### Key Entities

#### **Project**
- **Definition**: Major undertaking with start/end dates, budget, objectives
- **Master Data**: Project name, status, completion percentage, timeline
- **Linking**: Can be linked to Sales Orders, Purchase Orders
- **Purpose**: High-level project container

#### **Task**
- **Definition**: Individual work unit within project
- **Allocation**: Assigned to specific team member
- **Details**: 
  - Start and end date
  - Priority (High, Medium, Low)
  - Dependent tasks (sequential requirements)
  - Department/user assignment
  - Estimated hours
- **Purpose**: Break down project into manageable pieces

#### **Timesheet**
- **Definition**: Record of hours worked on specific tasks
- **Components**:
  - Activity (type of work)
  - Task/project reference
  - Hours spent
  - Billable flag
  - Date
- **Aggregation**: Can group by project/task for reporting
- **Purpose**: Track actual effort spent

#### **Project Cost**
- **Definition**: Tracking of expenses against project
- **Includes**: Direct costs (materials), labor (timesheets), overhead
- **Calculation**: Based on timesheets and expense records
- **Purpose**: Monitor project budget utilization

#### **Project Profitability**
- **Definition**: Analysis of project revenue vs. costs
- **Components**:
  - Revenue: From Sales Orders linked to project
  - Costs: From purchases, timesheets, expense claims
  - Profit: Revenue - Costs
- **Purpose**: Evaluate project financial performance

### Project Types

1. **Internal Projects**: Company initiatives (office setup, system implementation)
2. **Customer Projects**: Billable projects sold to customers
3. **Manufacturing Jobs**: Production orders treated as projects
4. **Service Projects**: Professional services engagements

### Project Workflow

```
1. Project Created
   ↓
2. Project Linked to Sales Order (if customer project)
   ↓
3. Tasks Created and Assigned to Team Members
   ↓
4. Team Works on Tasks
   ↓
5. Timesheets Submitted Weekly/Monthly
   ↓
6. Expenses Recorded (material purchases, expense claims)
   ↓
7. Project Cost Monitored Against Budget
   ↓
8. Project Profitability Calculated
   ↓
9. Project Completion Status Updated
   ↓
10. Final Project Profitability Report Generated
```

### Key Reports

| Report | Purpose |
|--------|---------|
| Project Summary | Overall project status, budget, timeline |
| Project Profitability | Revenue, costs, profit analysis |
| Task Summary | Individual task status and progress |
| Timesheet Analysis | Hours by employee, task, project |
| Project Cost Analysis | Detailed cost breakdown |

### Project Benefits

✓ Structured project organization  
✓ Resource allocation and utilization tracking  
✓ Budget control and cost monitoring  
✓ Timeline and deadline management  
✓ Profitability analysis  
✓ Integrated with sales and purchases for complete project view  

---

## 3.10 Website & E-Commerce Module

**Purpose**: Build and manage company website with e-commerce capabilities

**Official Guide**: [Website and E-Commerce](https://erpnext.com/erp-guide/website-and-ecommerce)

### Module Overview

| Aspect | Details |
|--------|---------|
| **Primary Focus** | Web presence, product catalog, online shopping, lead generation |
| **Key Users** | Marketing, web administrator, content creators |
| **Integration** | Syncs products from inventory, creates sales orders from shopping cart |
| **Core Value** | Direct customer access, self-service, brand presence |

### Website Components

#### **Web Page**
- **Definition**: Static content pages on website
- **Examples**: Home, About Us, Contact Us, Terms & Conditions
- **Features**: Title, content, images, SEO metadata
- **Purpose**: Provide company information

#### **Home Page**
- **Definition**: Landing page when visitor arrives at website
- **Importance**: First impression, critical for engagement
- **Content**: Hero section, featured products, company overview

#### **Blog Post**
- **Definition**: Informational articles published on website
- **Purpose**: Share knowledge, improve SEO, engage audience
- **Content**: Author, date, categories, content, images
- **Benefit**: Builds thought leadership

#### **Website Theme**
- **Definition**: Visual design template for website
- **Components**: Colors, fonts, layouts, styling
- **Customization**: Can be customized without coding
- **Purpose**: Brand consistency

#### **Website Settings**
- **Configuration**: Theme selection, logo, favicon, social media links
- **SEO**: Google indexing, analytics tracking
- **Features**: Enable/disable comments, chat, redirects
- **Purpose**: Global website configuration

#### **Website Route Meta**
- **Definition**: Meta tags for SEO optimization
- **Content**: Title, description, keywords, Open Graph tags
- **Purpose**: Improve search engine rankings and social sharing

### E-Commerce Components

#### **Product Page**
- **Definition**: Dedicated page for each product
- **Content**: Description, images, specifications, pricing
- **Linked To**: Item master from inventory
- **Dynamic**: Updates automatically when item changes
- **Purpose**: Present products to customers

#### **Product Listing**
- **Definition**: Catalog page showing multiple products
- **Features**: Filtering, sorting, search, pagination
- **Categories**: Organize by product type
- **Purpose**: Help customers discover products

#### **Shopping Cart**
- **Definition**: Virtual cart where customers add products
- **Features**:
  - Add/remove items
  - Quantity adjustment
  - Price recalculation
  - Apply coupon codes
  - Checkout
- **Impact**: Creates Sales Order when checked out
- **Purpose**: Enable self-service purchasing

#### **Webform**
- **Definition**: Form for website visitors to submit information
- **Examples**: Contact Us, Job Application, Support Request, Quote Request
- **Submission**: Data captured directly into ERP
- **Workflow**: Can trigger notifications, auto-responses
- **Purpose**: Capture leads and customer interactions

#### **Social Login**
- **Definition**: Allow users to sign in via social media (Google, Facebook, GitHub)
- **Benefits**: Easier user registration and login
- **Purpose**: Improve user experience, reduce friction

### Website Workflow

```
1. Website Structure Created (pages, theme)
   ↓
2. Company Information & Branding Configured
   ↓
3. Products Configured in Inventory
   ↓
4. Product Pages Automatically Generated
   ↓
5. Product Listing Created with Filters
   ↓
6. Shopping Cart Enabled for E-commerce
   ↓
7. Webforms Created (Contact, Support, Careers)
   ↓
8. SEO Meta Tags Added
   ↓
9. Social Login Enabled
   ↓
10. Website Live for Customer Access
```

### Key Features

#### **Page Builder**
- **Zero Code**: Create pages without coding
- **Drag & Drop**: Visual page building
- **Purpose**: Empower non-technical users to create content

#### **SEO Support**
- **Meta Tags**: Title, description, keywords
- **Sitemap**: Automatic XML sitemap generation
- **Mobile Responsive**: Built-in mobile optimization
- **Analytics**: Google Analytics integration
- **Purpose**: Improve search visibility

#### **Blog Engine**
- **Publishing**: Schedule posts for future publishing
- **Categories**: Organize posts by topic
- **Comments**: Reader engagement
- **Archives**: Historical post access
- **Purpose**: Regular content marketing

### E-Commerce Benefits

✓ Direct customer access (B2B2C)  
✓ Reduced intermediary costs  
✓ 24/7 storefront availability  
✓ Automatic inventory synchronization  
✓ Self-service lead capture  
✓ Integrated with sales and inventory  

---

# Part 4: Frontend Integration & Local Setup

## 4.1 Local ERPNext Deployment (frappe_docker)

Your local deployment at **http://localhost:8080** runs the complete ERPNext system in Docker containers.

### Accessing the Local Frontend

**URL**: http://localhost:8080  
**Default Credentials**: Check your `.env` file or setup documentation

### Module Access in Frontend

Each ERPNext module is accessible through:
1. **Sidebar Navigation**: Left panel with module sections
2. **Search Bar**: Quick search for any document or report
3. **Workspace**: Custom layouts for modules

### Frontend Module Layout

```
Home Dashboard
├── CRM
│   ├── Leads
│   ├── Opportunities  
│   ├── Campaigns
│   └── Reports
├── Selling
│   ├── Sales Orders
│   ├── Quotations
│   ├── Customers
│   └── Sales Reports
├── Buying
│   ├── Purchase Orders
│   ├── Suppliers
│   ├── Request for Quotation
│   └── Buying Reports
├── Stock
│   ├── Warehouses
│   ├── Items
│   ├── Stock Entries
│   ├── Delivery Notes
│   └── Stock Reports
├── Accounting
│   ├── Chart of Accounts
│   ├── Journal Entry
│   ├── Invoices
│   └── Financial Reports
├── Manufacturing
│   ├── Bill of Materials
│   ├── Work Orders
│   ├── Job Cards
│   └── Production Reports
├── HR
│   ├── Employees
│   ├── Leave
│   ├── Attendance
│   ├── Payroll
│   └── HR Reports
├── Assets
│   ├── Asset Master
│   ├── Maintenance
│   └── Asset Reports
├── Projects
│   ├── Projects
│   ├── Tasks
│   ├── Timesheets
│   └── Project Reports
└── Website
    ├── Website Settings
    ├── Web Pages
    ├── Products
    └── E-Commerce
```

## 4.2 Common Frontend Tasks

### Creating a Record

**Process**:
1. Navigate to module list (e.g., Sales → Sales Order)
2. Click "+ Add" or "+ New" button
3. Fill in required fields (marked with red asterisk)
4. Save as Draft (Ctrl+S)
5. Review and Submit (if workflow requires)

### Navigating Reports

**Access**:
1. Module → Reports section
2. Or search for specific report name
3. Apply filters to narrow data
4. Export to CSV/PDF if needed

### Customizing Views

**Custom Reports/Views**:
1. Module list view
2. Filter icon to add filters
3. "Save Filter" to create named view
4. Reuse filter next time

### Bulk Operations

**Bulk Updates**:
1. List view → Select records (checkbox)
2. Actions menu → Bulk operations
3. Update field across selected records

---

## 4.3 Integration Points Between Modules

### Module Data Flow

```
SALES FLOW:
CRM (Lead/Opportunity) 
  → Sales (Quotation → Sales Order)
  → Stock (Delivery Note)
  → Accounting (Sales Invoice)
  → [Optional] Projects (if project-linked)

PROCUREMENT FLOW:
Material Request
  → Buying (RFQ → Supplier Quotation → PO)
  → Stock (Purchase Receipt)
  → Accounting (Purchase Invoice)

MANUFACTURING FLOW:
Sales Order → Material Request
  → Production Planning
  → Manufacturing (Work Order → Job Card)
  → Stock (Stock Entries for materials)
  → Quality (Inspections)

HR FLOW:
Recruitment (Applicant → Job Offer → Appointment)
  → Employee Master
  → Leave Management
  → Attendance
  → Payroll (Salary Slip → Journal Entry to Accounting)

PROJECT FLOW:
Project → Tasks → Timesheets
  → Project Cost → Project Profitability
  → [Optional] Linked to Sales Order for billing
```

---

# Part 5: Quick Reference Index

## Module Quick Links

| Module | Primary Focus | Key Transactions | Key Users |
|--------|---------------|------------------|-----------|
| **CRM** | Lead/Opportunity management | Lead, Opportunity, Campaign | Sales managers, marketers |
| **Sales** | Order fulfillment | Quotation, SO, Delivery Note, SI | Sales executives, customers |
| **Procurement** | Supplier management | RFQ, PO, Purchase Receipt, PI | Procurement, inventory |
| **Accounting** | Financial records | JE, SI, PI, GL Reports | Accountants, CFO |
| **Inventory** | Stock management | Stock Entry, Receipt, Delivery | Warehouse, inventory |
| **Manufacturing** | Production | BOM, Work Order, Job Card | Production, shop floor |
| **HRMS** | Employee management | Employee, Leave, Salary, Payroll | HR, payroll |
| **Assets** | Fixed asset lifecycle | Asset, Maintenance, Depreciation | Finance, facilities |
| **Projects** | Project execution | Project, Task, Timesheet | Project managers |
| **Website** | Web presence | Web Page, Blog, Product, Cart | Marketing, IT |

## Key Document Statuses

### Universal Statuses
- **Draft**: Not yet submitted, can be edited/deleted
- **Submitted**: Locked, creates downstream documents
- **Amended**: Previous version modified (creates new version)
- **Cancelled**: Reversed, creates offsetting entries

### Specific Statuses

**Sales Order**: Draft → Submitted → Partially Delivered → Delivered → Closed  
**Purchase Order**: Draft → Submitted → Partially Received → Received → Closed  
**Work Order**: Draft → Submitted → In Progress → Completed → Closed  
**Leave Application**: Draft → Submitted → Approved/Rejected  
**Salary Slip**: Draft → Submitted → Paid  

---

# Part 6: Resources & Links

## Official Documentation

### Main Resources
- **ERPNext ERP Guide**: https://frappe.io/erpnext/erp-guide
- **Technical Documentation**: https://docs.frappe.io/
- **Frappe School**: https://frappe.school/ (video tutorials)
- **Community Forum**: https://discuss.frappe.io/

### Official Guide Chapters

#### Part 1: Understanding ERPs
- [Business Sustainability](https://erpnext.com/erp-guide/business-sustainability)
- [Why Use ERP](https://erpnext.com/erp-guide/why-and-what-erp)
- [Evaluating an ERP](https://erpnext.com/erp-guide/evaluating-an-erp)

#### Part 2: Implementation
- [Implementing an ERP](https://erpnext.com/erp-guide/implementing-an-erp)
- [Agile Implementation Plan](https://erpnext.com/erp-guide/constructing-agile-implementation-plan)
- [Understanding Current System](https://erpnext.com/erp-guide/understanding-current-system)
- [Configuring Your ERP](https://erpnext.com/erp-guide/configuring-your-erp-system)

#### Part 3: Modules
- [CRM](https://erpnext.com/erp-guide/crm-system)
- [Sales](https://erpnext.com/erp-guide/sales-system)
- [Procurement](https://erpnext.com/erp-guide/procurement-system)
- [Accounting](https://erpnext.com/erp-guide/accounting-system)
- [Inventory](https://erpnext.com/erp-guide/inventory-management)
- [Manufacturing](https://erpnext.com/erp-guide/manufacturing)
- [HRMS](https://erpnext.com/erp-guide/human-resource-management)
- [Assets](https://erpnext.com/erp-guide/asset-management)
- [Projects](https://erpnext.com/erp-guide/project-management)
- [Website & E-Commerce](https://erpnext.com/erp-guide/website-and-ecommerce)

### Video Resources
- **Frappe School**: https://frappe.school/courses
- **YouTube Channel**: Search "ERPNext Tutorial"

### Community
- **GitHub**: https://github.com/frappe/erpnext
- **Community Forum**: https://discuss.frappe.io/
- **Issue Tracker**: https://github.com/frappe/erpnext/issues

---

## Implementation Checklist

### Phase 1: Planning (Week 1-2)
- [ ] Define business requirements
- [ ] Identify all modules needed
- [ ] Create gap analysis document
- [ ] Assemble implementation team

### Phase 2: Configuration (Week 3-6)
- [ ] Set up Company and Chart of Accounts
- [ ] Create Fiscal Year and Accounting Periods
- [ ] Set up Cost Centers and Warehouses
- [ ] Configure master data (customers, suppliers, items)
- [ ] Set tax rules and accounting defaults

### Phase 3: Core Modules Setup (Week 7-12)
- [ ] Configure CRM processes
- [ ] Setup Sales workflow
- [ ] Setup Procurement workflow
- [ ] Setup Inventory/Warehouse operations
- [ ] Configure manufacturing (if applicable)
- [ ] Setup HRMS and payroll
- [ ] Configure Projects (if applicable)

### Phase 4: Testing (Week 13-14)
- [ ] Test core workflows
- [ ] Verify data integrity
- [ ] Validate reports and calculations
- [ ] User acceptance testing

### Phase 5: Go-Live (Week 15)
- [ ] Final data migration
- [ ] Staff training
- [ ] System goes live
- [ ] Support during initial period

---

## Key Implementation Tips

### Do's ✓
- Start with core modules (Sales, Procurement, Accounting)
- Get business stakeholder buy-in early
- Use agile/iterative approach
- Validate data quality thoroughly
- Train users extensively before go-live
- Document customizations and configurations
- Plan for ongoing support

### Don'ts ✗
- Don't try to implement all modules at once
- Don't force ERP to fit broken processes (fix first)
- Don't ignore data quality issues
- Don't underestimate training needs
- Don't skip testing phase
- Don't modify core ERP code
- Don't go live without proper support plan

---

## Glossary of Key Terms

| Term | Definition |
|------|-----------|
| **BOM** | Bill of Materials - list of components for a product |
| **CoA** | Chart of Accounts - accounting structure |
| **Cost Center** | Organizational unit for cost allocation |
| **DocType** | Document type in ERPNext (like a table/form) |
| **Fiscal Year** | Financial period (typically 12 months) |
| **GL** | General Ledger - complete accounting transaction record |
| **JE** | Journal Entry - accounting transaction |
| **KPI** | Key Performance Indicator - business metric |
| **Material Request** | Request to purchase, transfer, or manufacture items |
| **P&L** | Profit and Loss statement - income statement |
| **PO** | Purchase Order - binding supplier agreement |
| **RFQ** | Request for Quotation - supplier inquiry |
| **SI** | Sales Invoice - bill to customer |
| **SKU** | Stock Keeping Unit - unique item code |
| **SO** | Sales Order - binding customer agreement |
| **Workflow** | Sequence of business process steps |

---

## Version Information

- **Document Created**: 2026-07-18
- **Based on**: Official ERPNext ERP Guide
- **Coverage**: 10 Core Modules + Implementation Guidance
- **Deployment**: frappe_docker (local)
- **Access**: http://localhost:8080

---

## Document Maintenance

This document serves as a living reference. Keep it updated:

- Review new module releases quarterly
- Update with additional customizations from your implementation
- Add team-specific notes and processes
- Document any custom configurations
- Link to internal process documentation

---

**License Notice**: This document is a summary and reference guide. The official ERPNext documentation is licensed under CC-BY-SA 3.0. See https://frappe.io/ for official resources.

---

*Last Updated: 2026-07-18*  
*Next Review: 2026-10-18*

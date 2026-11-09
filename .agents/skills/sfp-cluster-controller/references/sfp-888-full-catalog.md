---
title: SFP-888 Full Catalog
description: Complete enumerated CWE-888 Software Fault Pattern (SFP) cluster taxonomy (23 Primary Clusters, 57 Secondary Clusters, 619 member CWEs).
doc_type: reference
status: active
last_updated: 2026-09-11
target_audience: ai
source: https://cwe.mitre.org/data/definitions/888.html (CWE version 4.20)
---
# SFP-888 Full Catalog

Agent uses this reference for the exhaustive per-CWE membership of every SFP Primary and Secondary Cluster. The main `sfp-cluster-controller` skill uses this file for detail lookups beyond its summary routing table.

Note: some CWE IDs (for example CWE-415, CWE-763) legitimately appear under more than one cluster in the official CWE-888 graph view; this is a documented feature of the source taxonomy, not a duplication error. CWE-900 does not appear in this view (a numbering gap between CWE-899 and CWE-901 in the official taxonomy).
## SFP Primary Cluster: Risky Values (CWE-885)
### SFP Secondary Cluster: Glitch in Computation (CWE-998)
- CWE-128: Wrap-around Error
- CWE-190: Integer Overflow or Wraparound
- CWE-191: Integer Underflow (Wrap or Wraparound)
- CWE-194: Unexpected Sign Extension
- CWE-195: Signed to Unsigned Conversion Error
- CWE-196: Unsigned to Signed Conversion Error
- CWE-197: Numeric Truncation Error
- CWE-369: Divide By Zero
- CWE-456: Missing Initialization of a Variable
- CWE-457: Use of Uninitialized Variable
- CWE-466: Return of Pointer Value Outside of Expected Range
- CWE-468: Incorrect Pointer Scaling
- CWE-475: Undefined Behavior for Input to API
- CWE-480: Use of Incorrect Operator
- CWE-481: Assigning instead of Comparing
- CWE-486: Comparison of Classes by Name
- CWE-562: Return of Stack Variable Address
- CWE-570: Expression is Always False
- CWE-571: Expression is Always True
- CWE-579: J2EE Bad Practices: Non-serializable Object Stored in Session
- CWE-587: Assignment of a Fixed Address to a Pointer
- CWE-594: J2EE Framework: Saving Unserializable Objects to Disk
- CWE-597: Use of Wrong Operator in String Comparison
- CWE-628: Function Call with Incorrectly Specified Arguments
- CWE-681: Incorrect Conversion between Numeric Types
- CWE-683: Function Call With Incorrect Order of Arguments
- CWE-685: Function Call With Incorrect Number of Arguments
- CWE-686: Function Call With Incorrect Argument Type
- CWE-688: Function Call With Incorrect Variable or Reference as Argument
- CWE-704: Incorrect Type Conversion or Cast
- CWE-768: Incorrect Short Circuit Evaluation

## SFP Primary Cluster: Unused entities (CWE-886)
- CWE-482: Comparing instead of Assigning
- CWE-561: Dead Code
- CWE-563: Assignment to Variable without Use

## SFP Primary Cluster: API (CWE-887)
### SFP Secondary Cluster: Use of an Improper API (CWE-1001)
- CWE-111: Direct Use of Unsafe JNI
- CWE-227: 7PK - API Abuse
- CWE-242: Use of Inherently Dangerous Function
- CWE-245: J2EE Bad Practices: Direct Management of Connections
- CWE-246: J2EE Bad Practices: Direct Use of Sockets
- CWE-382: J2EE Bad Practices: Use of System.exit()
- CWE-383: J2EE Bad Practices: Direct Use of Threads
- CWE-432: Dangerous Signal Handler not Disabled During Sensitive Operations
- CWE-439: Behavioral Change in New Version or Environment
- CWE-440: Expected Behavior Violation
- CWE-474: Use of Function with Inconsistent Implementations
- CWE-477: Use of Obsolete Function
- CWE-479: Signal Handler Use of a Non-reentrant Function
- CWE-558: Use of getlogin() in Multithreaded Application
- CWE-572: Call to Thread run() instead of start()
- CWE-573: Improper Following of Specification by Caller
- CWE-574: EJB Bad Practices: Use of Synchronization Primitives
- CWE-575: EJB Bad Practices: Use of AWT Swing
- CWE-576: EJB Bad Practices: Use of Java I/O
- CWE-577: EJB Bad Practices: Use of Sockets
- CWE-578: EJB Bad Practices: Use of Class Loader
- CWE-586: Explicit Call to Finalize()
- CWE-589: Call to Non-ubiquitous API
- CWE-617: Reachable Assertion
- CWE-676: Use of Potentially Dangerous Function
- CWE-684: Incorrect Provision of Specified Functionality
- CWE-695: Use of Low-Level Functionality
- CWE-758: Reliance on Undefined, Unspecified, or Implementation-Defined Behavior

## SFP Primary Cluster: Exception Management (CWE-889)
### SFP Secondary Cluster: Ambiguous Exception Type (CWE-960)
- CWE-396: Declaration of Catch for Generic Exception
- CWE-397: Declaration of Throws for Generic Exception
### SFP Secondary Cluster: Incorrect Exception Behavior (CWE-961)
- CWE-392: Missing Report of Error Condition
- CWE-393: Return of Wrong Status Code
- CWE-455: Non-exit on Failed Initialization
- CWE-460: Improper Cleanup on Thrown Exception
- CWE-544: Missing Standardized Error Handling Mechanism
- CWE-584: Return Inside Finally Block
- CWE-636: Not Failing Securely ('Failing Open')
- CWE-703: Improper Check or Handling of Exceptional Conditions
### SFP Secondary Cluster: Unchecked Status Condition (CWE-962)
- CWE-248: Uncaught Exception
- CWE-252: Unchecked Return Value
- CWE-253: Incorrect Check of Function Return Value
- CWE-273: Improper Check for Dropped Privileges
- CWE-280: Improper Handling of Insufficient Permissions or Privileges
- CWE-372: Incomplete Internal State Distinction
- CWE-390: Detection of Error Condition Without Action
- CWE-391: Unchecked Error Condition
- CWE-394: Unexpected Status Code or Return Value
- CWE-395: Use of NullPointerException Catch to Detect NULL Pointer Dereference
- CWE-431: Missing Handler
- CWE-478: Missing Default Case in Multiple Condition Expression
- CWE-484: Omitted Break Statement in Switch
- CWE-600: Uncaught Exception in Servlet
- CWE-665: Improper Initialization
- CWE-754: Improper Check for Unusual or Exceptional Conditions
- CWE-755: Improper Handling of Exceptional Conditions

## SFP Primary Cluster: Memory Access (CWE-890)
### SFP Secondary Cluster: Faulty Buffer Access (CWE-970)
- CWE-118: Incorrect Access of Indexable Resource ('Range Error')
- CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer
- CWE-120: Buffer Copy without Checking Size of Input ('Classic Buffer Overflow')
- CWE-121: Stack-based Buffer Overflow
- CWE-122: Heap-based Buffer Overflow
- CWE-123: Write-what-where Condition
- CWE-124: Buffer Underwrite ('Buffer Underflow')
- CWE-125: Out-of-bounds Read
- CWE-126: Buffer Over-read
- CWE-127: Buffer Under-read
- CWE-129: Improper Validation of Array Index
### SFP Secondary Cluster: Faulty Pointer Use (CWE-971)
- CWE-469: Use of Pointer Subtraction to Determine Size
- CWE-476: NULL Pointer Dereference
- CWE-588: Attempt to Access Child of a Non-structure Pointer
### SFP Secondary Cluster: Faulty String Expansion (CWE-972)
- CWE-785: Use of Path Manipulation Function without Maximum-sized Buffer
### SFP Secondary Cluster: Improper NULL Termination (CWE-973)
- CWE-170: Improper Null Termination
### SFP Secondary Cluster: Incorrect Buffer Length Computation (CWE-974)
- CWE-131: Incorrect Calculation of Buffer Size
- CWE-135: Incorrect Calculation of Multi-Byte String Length
- CWE-251: Often Misused: String Management
- CWE-467: Use of sizeof() on a Pointer Type

## SFP Primary Cluster: Memory Management (CWE-891)
### SFP Secondary Cluster: Faulty Memory Release (CWE-969)
- CWE-415: Double Free
- CWE-590: Free of Memory not on the Heap
- CWE-761: Free of Pointer not at Start of Buffer
- CWE-763: Release of Invalid Pointer or Reference

## SFP Primary Cluster: Resource Management (CWE-892)
### SFP Secondary Cluster: Failure to Release Resource (CWE-982)
- CWE-404: Improper Resource Shutdown or Release
- CWE-459: Incomplete Cleanup
- CWE-771: Missing Reference to Active Allocated Resource
- CWE-772: Missing Release of Resource after Effective Lifetime
- CWE-773: Missing Reference to Active File Descriptor or Handle
- CWE-775: Missing Release of File Descriptor or Handle after Effective Lifetime
### SFP Secondary Cluster: Faulty Resource Use (CWE-983)
- CWE-416: Use After Free
- CWE-672: Operation on a Resource after Expiration or Release
### SFP Secondary Cluster: Life Cycle (CWE-984)
- CWE-664: Improper Control of a Resource Through its Lifetime
- CWE-666: Operation on Resource in Wrong Phase of Lifetime
- CWE-675: Multiple Operations on Resource in Single-Operation Context
- CWE-694: Use of Multiple Resources with Duplicate Identifier
### SFP Secondary Cluster: Unrestricted Consumption (CWE-985)
- CWE-400: Uncontrolled Resource Consumption
- CWE-674: Uncontrolled Recursion
- CWE-770: Allocation of Resources Without Limits or Throttling
- CWE-774: Allocation of File Descriptors or Handles Without Limits or Throttling

## SFP Primary Cluster: Path Resolution (CWE-893)
### SFP Secondary Cluster: Failed Chroot Jail (CWE-979)
- CWE-243: Creation of chroot Jail Without Changing Working Directory
### SFP Secondary Cluster: Link in Resource Name Resolution (CWE-980)
- CWE-386: Symbolic Name not Mapping to Correct Object
- CWE-59: Improper Link Resolution Before File Access ('Link Following')
- CWE-610: Externally Controlled Reference to a Resource in Another Sphere
- CWE-62: UNIX Hard Link
- CWE-64: Windows Shortcut Following (.LNK)
- CWE-65: Windows Hard Link
### SFP Secondary Cluster: Path Traversal (CWE-981)
- CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')
- CWE-23: Relative Path Traversal
- CWE-24: Path Traversal: '../filedir'
- CWE-25: Path Traversal: '/../filedir'
- CWE-26: Path Traversal: '/dir/../filename'
- CWE-27: Path Traversal: 'dir/../../filename'
- CWE-28: Path Traversal: '..\filedir'
- CWE-29: Path Traversal: '\..\filename'
- CWE-30: Path Traversal: '\dir\..\filename'
- CWE-31: Path Traversal: 'dir\..\..\filename'
- CWE-32: Path Traversal: '...' (Triple Dot)
- CWE-33: Path Traversal: '....' (Multiple Dot)
- CWE-34: Path Traversal: '....//'
- CWE-35: Path Traversal: '.../...//'
- CWE-36: Absolute Path Traversal
- CWE-37: Path Traversal: '/absolute/pathname/here'
- CWE-38: Path Traversal: '\absolute\pathname\here'
- CWE-39: Path Traversal: 'C:dirname'
- CWE-40: Path Traversal: '\\UNC\share\name\' (Windows UNC Share)
- CWE-41: Improper Resolution of Path Equivalence
- CWE-42: Path Equivalence: 'filename.' (Trailing Dot)
- CWE-428: Unquoted Search Path or Element
- CWE-43: Path Equivalence: 'filename....' (Multiple Trailing Dot)
- CWE-44: Path Equivalence: 'file.name' (Internal Dot)
- CWE-45: Path Equivalence: 'file...name' (Multiple Internal Dot)
- CWE-46: Path Equivalence: 'filename ' (Trailing Space)
- CWE-47: Path Equivalence: ' filename' (Leading Space)
- CWE-48: Path Equivalence: 'file name' (Internal Whitespace)
- CWE-49: Path Equivalence: 'filename/' (Trailing Slash)
- CWE-50: Path Equivalence: '//multiple/leading/slash'
- CWE-51: Path Equivalence: '/multiple//internal/slash'
- CWE-52: Path Equivalence: '/multiple/trailing/slash//'
- CWE-53: Path Equivalence: '\multiple\\internal\backslash'
- CWE-54: Path Equivalence: 'filedir\' (Trailing Backslash)
- CWE-55: Path Equivalence: '/./' (Single Dot Directory)
- CWE-56: Path Equivalence: 'filedir*' (Wildcard)
- CWE-57: Path Equivalence: 'fakedir/../realdir/filename'
- CWE-58: Path Equivalence: Windows 8.3 Filename
- CWE-66: Improper Handling of File Names that Identify Virtual Resources
- CWE-67: Improper Handling of Windows Device Names
- CWE-706: Use of Incorrectly-Resolved Name or Reference
- CWE-72: Improper Handling of Apple HFS+ Alternate Data Stream Path
- CWE-73: External Control of File Name or Path

## SFP Primary Cluster: Synchronization (CWE-894)
### SFP Secondary Cluster: Missing Lock (CWE-986)
- CWE-364: Signal Handler Race Condition
- CWE-366: Race Condition within a Thread
- CWE-368: Context Switching Race Condition
- CWE-413: Improper Resource Locking
- CWE-414: Missing Lock Check
- CWE-543: Use of Singleton Pattern Without Synchronization in a Multithreaded Context
- CWE-567: Unsynchronized Access to Shared Data in a Multithreaded Context
- CWE-609: Double-Checked Locking
- CWE-662: Improper Synchronization
- CWE-663: Use of a Non-reentrant Function in a Concurrent Context
- CWE-667: Improper Locking
### SFP Secondary Cluster: Multiple Locks/Unlocks (CWE-987)
- CWE-585: Empty Synchronized Block
- CWE-764: Multiple Locks of a Critical Resource
- CWE-765: Multiple Unlocks of a Critical Resource
### SFP Secondary Cluster: Race Condition Window (CWE-988)
- CWE-362: Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition')
- CWE-363: Race Condition Enabling Link Following
- CWE-367: Time-of-check Time-of-use (TOCTOU) Race Condition
- CWE-370: Missing Check for Certificate Revocation after Initial Check
- CWE-638: Not Using Complete Mediation
### SFP Secondary Cluster: Unrestricted Lock (CWE-989)
- CWE-412: Unrestricted Externally Accessible Lock

## SFP Primary Cluster: Information Leak (CWE-895)
### SFP Secondary Cluster: Exposed Data (CWE-963)
- CWE-11: ASP.NET Misconfiguration: Creating Debug Binary
- CWE-117: Improper Output Neutralization for Logs
- CWE-12: ASP.NET Misconfiguration: Missing Custom Error Page
- CWE-13: ASP.NET Misconfiguration: Password in Configuration File
- CWE-14: Compiler Removal of Code to Clear Buffers
- CWE-200: Exposure of Sensitive Information to an Unauthorized Actor
- CWE-201: Insertion of Sensitive Information Into Sent Data
- CWE-209: Generation of Error Message Containing Sensitive Information
- CWE-210: Self-generated Error Message Containing Sensitive Information
- CWE-211: Externally-Generated Error Message Containing Sensitive Information
- CWE-212: Improper Removal of Sensitive Information Before Storage or Transfer
- CWE-213: Exposure of Sensitive Information Due to Incompatible Policies
- CWE-214: Invocation of Process Using Visible Sensitive Information
- CWE-215: Insertion of Sensitive Information Into Debugging Code
- CWE-219: Storage of File with Sensitive Data Under Web Root
- CWE-220: Storage of File With Sensitive Data Under FTP Root
- CWE-226: Sensitive Information in Resource Not Removed Before Reuse
- CWE-244: Improper Clearing of Heap Memory Before Release ('Heap Inspection')
- CWE-256: Plaintext Storage of a Password
- CWE-257: Storing Passwords in a Recoverable Format
- CWE-260: Password in Configuration File
- CWE-311: Missing Encryption of Sensitive Data
- CWE-312: Cleartext Storage of Sensitive Information
- CWE-313: Cleartext Storage in a File or on Disk
- CWE-314: Cleartext Storage in the Registry
- CWE-315: Cleartext Storage of Sensitive Information in a Cookie
- CWE-316: Cleartext Storage of Sensitive Information in Memory
- CWE-317: Cleartext Storage of Sensitive Information in GUI
- CWE-318: Cleartext Storage of Sensitive Information in Executable
- CWE-319: Cleartext Transmission of Sensitive Information
- CWE-374: Passing Mutable Objects to an Untrusted Method
- CWE-375: Returning a Mutable Object to an Untrusted Caller
- CWE-402: Transmission of Private Resources into a New Sphere ('Resource Leak')
- CWE-403: Exposure of File Descriptor to Unintended Control Sphere ('File Descriptor Leak')
- CWE-433: Unparsed Raw Web Content Delivery
- CWE-495: Private Data Structure Returned From A Public Method
- CWE-497: Exposure of Sensitive System Information to an Unauthorized Control Sphere
- CWE-498: Cloneable Class Containing Sensitive Information
- CWE-499: Serializable Class Containing Sensitive Data
- CWE-5: J2EE Misconfiguration: Data Transmission Without Encryption
- CWE-501: Trust Boundary Violation
- CWE-522: Insufficiently Protected Credentials
- CWE-523: Unprotected Transport of Credentials
- CWE-526: Cleartext Storage of Sensitive Information in an Environment Variable
- CWE-527: Exposure of Version-Control Repository to an Unauthorized Control Sphere
- CWE-528: Exposure of Core Dump File to an Unauthorized Control Sphere
- CWE-529: Exposure of Access Control List Files to an Unauthorized Control Sphere
- CWE-530: Exposure of Backup File to an Unauthorized Control Sphere
- CWE-532: Insertion of Sensitive Information into Log File
- CWE-535: Exposure of Information Through Shell Error Message
- CWE-536: Servlet Runtime Error Message Containing Sensitive Information
- CWE-537: Java Runtime Error Message Containing Sensitive Information
- CWE-538: Insertion of Sensitive Information into Externally-Accessible File or Directory
- CWE-539: Use of Persistent Cookies Containing Sensitive Information
- CWE-540: Inclusion of Sensitive Information in Source Code
- CWE-541: Inclusion of Sensitive Information in an Include File
- CWE-546: Suspicious Comment
- CWE-548: Exposure of Information Through Directory Listing
- CWE-550: Server-generated Error Message Containing Sensitive Information
- CWE-552: Files or Directories Accessible to External Parties
- CWE-555: J2EE Misconfiguration: Plaintext Password in Configuration File
- CWE-591: Sensitive Data Storage in Improperly Locked Memory
- CWE-598: Use of HTTP Request With Sensitive Query String
- CWE-607: Public Static Final Field References Mutable Object
- CWE-612: Improper Authorization of Index Containing Sensitive Information
- CWE-615: Inclusion of Sensitive Information in Source Code Comments
- CWE-642: External Control of Critical State Data
- CWE-668: Exposure of Resource to Wrong Sphere
- CWE-669: Incorrect Resource Transfer Between Spheres
- CWE-7: J2EE Misconfiguration: Missing Custom Error Page
- CWE-756: Missing Custom Error Page
- CWE-767: Access to Critical Private Variable via Public Method
- CWE-8: J2EE Misconfiguration: Entity Bean Declared Remote
### SFP Secondary Cluster: Exposure Temporary File (CWE-964)
- CWE-377: Insecure Temporary File
- CWE-378: Creation of Temporary File With Insecure Permissions
- CWE-379: Creation of Temporary File in Directory with Insecure Permissions
### SFP Secondary Cluster: Insecure Session Management (CWE-965)
- CWE-488: Exposure of Data Element to Wrong Session
- CWE-524: Use of Cache Containing Sensitive Information
- CWE-6: J2EE Misconfiguration: Insufficient Session-ID Length
### SFP Secondary Cluster: Other Exposures (CWE-966)
- CWE-453: Insecure Default Variable Initialization
- CWE-487: Reliance on Package-level Scope
- CWE-492: Use of Inner Class Containing Sensitive Data
- CWE-525: Use of Web Browser Cache Containing Sensitive Information
- CWE-614: Sensitive Cookie in HTTPS Session Without 'Secure' Attribute
- CWE-651: Exposure of WSDL File Containing Sensitive Information
### SFP Secondary Cluster: State Disclosure (CWE-967)
- CWE-202: Exposure of Sensitive Information Through Data Queries
- CWE-203: Observable Discrepancy
- CWE-204: Observable Response Discrepancy
- CWE-205: Observable Behavioral Discrepancy
- CWE-206: Observable Internal Behavioral Discrepancy
- CWE-207: Observable Behavioral Discrepancy With Equivalent Products
- CWE-208: Observable Timing Discrepancy

## SFP Primary Cluster: Tainted Input (CWE-896)
### SFP Secondary Cluster: Tainted Input to Command (CWE-990)
- CWE-102: Struts: Duplicate Validation Forms
- CWE-103: Struts: Incomplete validate() Method Definition
- CWE-104: Struts: Form Bean Does Not Extend Validation Class
- CWE-105: Struts: Form Field Without Validator
- CWE-106: Struts: Plug-in Framework not in Use
- CWE-107: Struts: Unused Validation Form
- CWE-108: Struts: Unvalidated Action Form
- CWE-109: Struts: Validator Turned Off
- CWE-110: Struts: Validator Without Form Field
- CWE-112: Missing XML Validation
- CWE-113: Improper Neutralization of CRLF Sequences in HTTP Headers ('HTTP Request/Response Splitting')
- CWE-130: Improper Handling of Length Parameter Inconsistency
- CWE-134: Use of Externally-Controlled Format String
- CWE-138: Improper Neutralization of Special Elements
- CWE-140: Improper Neutralization of Delimiters
- CWE-141: Improper Neutralization of Parameter/Argument Delimiters
- CWE-142: Improper Neutralization of Value Delimiters
- CWE-143: Improper Neutralization of Record Delimiters
- CWE-144: Improper Neutralization of Line Delimiters
- CWE-145: Improper Neutralization of Section Delimiters
- CWE-146: Improper Neutralization of Expression/Command Delimiters
- CWE-147: Improper Neutralization of Input Terminators
- CWE-148: Improper Neutralization of Input Leaders
- CWE-149: Improper Neutralization of Quoting Syntax
- CWE-150: Improper Neutralization of Escape, Meta, or Control Sequences
- CWE-151: Improper Neutralization of Comment Delimiters
- CWE-152: Improper Neutralization of Macro Symbols
- CWE-153: Improper Neutralization of Substitution Characters
- CWE-154: Improper Neutralization of Variable Name Delimiters
- CWE-155: Improper Neutralization of Wildcards or Matching Symbols
- CWE-156: Improper Neutralization of Whitespace
- CWE-157: Failure to Sanitize Paired Delimiters
- CWE-158: Improper Neutralization of Null Byte or NUL Character
- CWE-159: Improper Handling of Invalid Use of Special Elements
- CWE-160: Improper Neutralization of Leading Special Elements
- CWE-161: Improper Neutralization of Multiple Leading Special Elements
- CWE-162: Improper Neutralization of Trailing Special Elements
- CWE-163: Improper Neutralization of Multiple Trailing Special Elements
- CWE-164: Improper Neutralization of Internal Special Elements
- CWE-165: Improper Neutralization of Multiple Internal Special Elements
- CWE-183: Permissive List of Allowed Inputs
- CWE-184: Incomplete List of Disallowed Inputs
- CWE-185: Incorrect Regular Expression
- CWE-186: Overly Restrictive Regular Expression
- CWE-444: Inconsistent Interpretation of HTTP Requests ('HTTP Request/Response Smuggling')
- CWE-553: Command Shell in Externally Accessible Directory
- CWE-554: ASP.NET Misconfiguration: Not Using Input Validation Framework
- CWE-564: SQL Injection: Hibernate
- CWE-601: URL Redirection to Untrusted Site ('Open Redirect')
- CWE-611: Improper Restriction of XML External Entity Reference
- CWE-619: Dangling Database Cursor ('Cursor Injection')
- CWE-621: Variable Extraction Error
- CWE-624: Executable Regular Expression Error
- CWE-625: Permissive Regular Expression
- CWE-626: Null Byte Interaction Error (Poison Null Byte)
- CWE-627: Dynamic Variable Evaluation
- CWE-641: Improper Restriction of Names for Files and Other Resources
- CWE-643: Improper Neutralization of Data within XPath Expressions ('XPath Injection')
- CWE-644: Improper Neutralization of HTTP Headers for Scripting Syntax
- CWE-646: Reliance on File Name or Extension of Externally-Supplied File
- CWE-652: Improper Neutralization of Data within XQuery Expressions ('XQuery Injection')
- CWE-687: Function Call With Incorrectly Specified Argument Value
- CWE-707: Improper Neutralization
- CWE-74: Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection')
- CWE-75: Failure to Sanitize Special Elements into a Different Plane (Special Element Injection)
- CWE-76: Improper Neutralization of Equivalent Special Elements
- CWE-77: Improper Neutralization of Special Elements used in a Command ('Command Injection')
- CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')
- CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')
- CWE-80: Improper Neutralization of Script-Related HTML Tags in a Web Page (Basic XSS)
- CWE-81: Improper Neutralization of Script in an Error Message Web Page
- CWE-82: Improper Neutralization of Script in Attributes of IMG Tags in a Web Page
- CWE-83: Improper Neutralization of Script in Attributes in a Web Page
- CWE-84: Improper Neutralization of Encoded URI Schemes in a Web Page
- CWE-85: Doubled Character XSS Manipulations
- CWE-86: Improper Neutralization of Invalid Characters in Identifiers in Web Pages
- CWE-87: Improper Neutralization of Alternate XSS Syntax
- CWE-88: Improper Neutralization of Argument Delimiters in a Command ('Argument Injection')
- CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')
- CWE-90: Improper Neutralization of Special Elements used in an LDAP Query ('LDAP Injection')
- CWE-91: XML Injection (aka Blind XPath Injection)
- CWE-93: Improper Neutralization of CRLF Sequences ('CRLF Injection')
- CWE-95: Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection')
- CWE-96: Improper Neutralization of Directives in Statically Saved Code ('Static Code Injection')
- CWE-97: Improper Neutralization of Server-Side Includes (SSI) Within a Web Page
- CWE-99: Improper Control of Resource Identifiers ('Resource Injection')
### SFP Secondary Cluster: Tainted Input to Environment (CWE-991)
- CWE-114: Process Control
- CWE-427: Uncontrolled Search Path Element
- CWE-470: Use of Externally-Controlled Input to Select Classes or Code ('Unsafe Reflection')
- CWE-471: Modification of Assumed-Immutable Data (MAID)
- CWE-472: External Control of Assumed-Immutable Web Parameter
- CWE-473: PHP External Variable Modification
- CWE-494: Download of Code Without Integrity Check
- CWE-622: Improper Validation of Function Hook Arguments
- CWE-673: External Influence of Sphere Definition
- CWE-94: Improper Control of Generation of Code ('Code Injection')
### SFP Secondary Cluster: Faulty Input Transformation (CWE-992)
- CWE-116: Improper Encoding or Escaping of Output
- CWE-166: Improper Handling of Missing Special Element
- CWE-167: Improper Handling of Additional Special Element
- CWE-168: Improper Handling of Inconsistent Special Elements
- CWE-172: Encoding Error
- CWE-173: Improper Handling of Alternate Encoding
- CWE-174: Double Decoding of the Same Data
- CWE-175: Improper Handling of Mixed Encoding
- CWE-176: Improper Handling of Unicode Encoding
- CWE-177: Improper Handling of URL Encoding (Hex Encoding)
- CWE-178: Improper Handling of Case Sensitivity
- CWE-179: Incorrect Behavior Order: Early Validation
- CWE-180: Incorrect Behavior Order: Validate Before Canonicalize
- CWE-181: Incorrect Behavior Order: Validate Before Filter
- CWE-182: Collapse of Data into Unsafe Value
### SFP Secondary Cluster: Incorrect Input Handling (CWE-993)
- CWE-198: Use of Incorrect Byte Ordering
- CWE-228: Improper Handling of Syntactically Invalid Structure
- CWE-229: Improper Handling of Values
- CWE-230: Improper Handling of Missing Values
- CWE-231: Improper Handling of Extra Values
- CWE-232: Improper Handling of Undefined Values
- CWE-233: Improper Handling of Parameters
- CWE-234: Failure to Handle Missing Parameter
- CWE-235: Improper Handling of Extra Parameters
- CWE-236: Improper Handling of Undefined Parameters
- CWE-237: Improper Handling of Structural Elements
- CWE-238: Improper Handling of Incomplete Structural Elements
- CWE-239: Failure to Handle Incomplete Element
- CWE-240: Improper Handling of Inconsistent Structural Elements
- CWE-241: Improper Handling of Unexpected Data Type
- CWE-351: Insufficient Type Distinction
- CWE-354: Improper Validation of Integrity Check Value
### SFP Secondary Cluster: Tainted Input to Variable (CWE-994)
- CWE-15: External Control of System or Configuration Setting
- CWE-20: Improper Input Validation
- CWE-454: External Initialization of Trusted Variables or Data Stores
- CWE-496: Public Data Assigned to Private Array-Typed Field
- CWE-502: Deserialization of Untrusted Data
- CWE-566: Authorization Bypass Through User-Controlled SQL Primary Key
- CWE-606: Unchecked Input for Loop Condition
- CWE-616: Incomplete Identification of Uploaded File Variables (PHP)

## SFP Primary Cluster: Entry Points (CWE-897)
### SFP Secondary Cluster: Unexpected Entry Points (CWE-1002)
- CWE-489: Active Debug Code
- CWE-491: Public cloneable() Method Without Final ('Object Hijack')
- CWE-493: Critical Public Variable Without Final Modifier
- CWE-500: Public Static Field Not Marked Final
- CWE-531: Inclusion of Sensitive Information in Test Code
- CWE-568: finalize() Method Without super.finalize()
- CWE-580: clone() Method Without super.clone()
- CWE-582: Array Declared Public, Final, and Static
- CWE-583: finalize() Method Declared Public
- CWE-608: Struts: Non-private Field in ActionForm Class
- CWE-766: Critical Data Element Declared Public

## SFP Primary Cluster: Authentication (CWE-898)
### SFP Secondary Cluster: Authentication Bypass (CWE-947)
- CWE-287: Improper Authentication
- CWE-288: Authentication Bypass Using an Alternate Path or Channel
- CWE-289: Authentication Bypass by Alternate Name
- CWE-303: Incorrect Implementation of Authentication Algorithm
- CWE-304: Missing Critical Step in Authentication
- CWE-305: Authentication Bypass by Primary Weakness
- CWE-308: Use of Single-factor Authentication
- CWE-309: Use of Password System for Primary Authentication
- CWE-603: Use of Client-Side Authentication
### SFP Secondary Cluster: Digital Certificate (CWE-948)
- CWE-296: Improper Following of a Certificate's Chain of Trust
- CWE-297: Improper Validation of Certificate with Host Mismatch
- CWE-298: Improper Validation of Certificate Expiration
- CWE-299: Improper Check for Certificate Revocation
- CWE-593: Authentication Bypass: OpenSSL CTX Object Modified after SSL Objects are Created
- CWE-599: Missing Validation of OpenSSL Certificate
### SFP Secondary Cluster: Faulty Endpoint Authentication (CWE-949)
- CWE-293: Using Referer Field for Authentication
- CWE-302: Authentication Bypass by Assumed-Immutable Data
- CWE-345: Insufficient Verification of Data Authenticity
- CWE-346: Origin Validation Error
- CWE-350: Reliance on Reverse DNS Resolution for a Security-Critical Action
- CWE-360: Trust of System Event Data
- CWE-551: Incorrect Behavior Order: Authorization Before Parsing and Canonicalization
- CWE-565: Reliance on Cookies without Validation and Integrity Checking
- CWE-647: Use of Non-Canonical URL Paths for Authorization Decisions
### SFP Secondary Cluster: Hardcoded Sensitive Data (CWE-950)
- CWE-258: Empty Password in Configuration File
- CWE-259: Use of Hard-coded Password
- CWE-321: Use of Hard-coded Cryptographic Key
- CWE-547: Use of Hard-coded, Security-relevant Constants
### SFP Secondary Cluster: Insecure Authentication Policy (CWE-951)
- CWE-262: Not Using Password Aging
- CWE-263: Password Aging with Long Expiration
- CWE-521: Weak Password Requirements
- CWE-556: ASP.NET Misconfiguration: Use of Identity Impersonation
- CWE-613: Insufficient Session Expiration
- CWE-645: Overly Restrictive Account Lockout Mechanism
### SFP Secondary Cluster: Missing Authentication (CWE-952)
- CWE-306: Missing Authentication for Critical Function
- CWE-620: Unverified Password Change
### SFP Secondary Cluster: Missing Endpoint Authentication (CWE-953)
- CWE-422: Unprotected Windows Messaging Channel ('Shatter')
- CWE-425: Direct Request ('Forced Browsing')
### SFP Secondary Cluster: Multiple Binds to the Same Port (CWE-954)
- CWE-605: Multiple Binds to the Same Port
### SFP Secondary Cluster: Unrestricted Authentication (CWE-955)
- CWE-307: Improper Restriction of Excessive Authentication Attempts

## SFP Primary Cluster: Access Control (CWE-899)
### SFP Secondary Cluster: Access Management (CWE-944)
- CWE-282: Improper Ownership Management
- CWE-283: Unverified Ownership
- CWE-284: Improper Access Control
- CWE-286: Incorrect User Management
- CWE-708: Incorrect Ownership Assignment
### SFP Secondary Cluster: Insecure Resource Access (CWE-945)
- CWE-285: Improper Authorization
- CWE-424: Improper Protection of Alternate Path
- CWE-639: Authorization Bypass Through User-Controlled Key
- CWE-650: Trusting HTTP Permission Methods on the Server Side
### SFP Secondary Cluster: Insecure Resource Permissions (CWE-946)
- CWE-276: Incorrect Default Permissions
- CWE-277: Insecure Inherited Permissions
- CWE-278: Insecure Preserved Inherited Permissions
- CWE-279: Incorrect Execution-Assigned Permissions
- CWE-281: Improper Preservation of Permissions
- CWE-560: Use of umask() with chmod-style Argument
- CWE-732: Incorrect Permission Assignment for Critical Resource

## SFP Primary Cluster: Privilege (CWE-901)
- CWE-250: Execution with Unnecessary Privileges
- CWE-266: Incorrect Privilege Assignment
- CWE-267: Privilege Defined With Unsafe Actions
- CWE-268: Privilege Chaining
- CWE-269: Improper Privilege Management
- CWE-270: Privilege Context Switching Error
- CWE-271: Privilege Dropping / Lowering Errors
- CWE-272: Least Privilege Violation
- CWE-274: Improper Handling of Insufficient Privileges
- CWE-520: .NET Misconfiguration: Use of Impersonation
- CWE-653: Improper Isolation or Compartmentalization
- CWE-9: J2EE Misconfiguration: Weak Access Permissions for EJB Methods

## SFP Primary Cluster: Channel (CWE-902)
### SFP Secondary Cluster: Channel Attack (CWE-956)
- CWE-290: Authentication Bypass by Spoofing
- CWE-294: Authentication Bypass by Capture-replay
- CWE-300: Channel Accessible by Non-Endpoint
- CWE-301: Reflection Attack in an Authentication Protocol
- CWE-419: Unprotected Primary Channel
- CWE-420: Unprotected Alternate Channel
- CWE-421: Race Condition During Access to Alternate Channel
- CWE-441: Unintended Proxy or Intermediary ('Confused Deputy')
### SFP Secondary Cluster: Protocol Error (CWE-957)
- CWE-353: Missing Support for Integrity Check
- CWE-435: Improper Interaction Between Multiple Correctly-Behaving Entities
- CWE-436: Interpretation Conflict
- CWE-437: Incomplete Model of Endpoint Features
- CWE-757: Selection of Less-Secure Algorithm During Negotiation ('Algorithm Downgrade')

## SFP Primary Cluster: Cryptography (CWE-903)
### SFP Secondary Cluster: Broken Cryptography (CWE-958)
- CWE-325: Missing Cryptographic Step
- CWE-327: Use of a Broken or Risky Cryptographic Algorithm
- CWE-328: Use of Weak Hash
- CWE-759: Use of a One-Way Hash without a Salt
- CWE-760: Use of a One-Way Hash with a Predictable Salt
### SFP Secondary Cluster: Weak Cryptography (CWE-959)
- CWE-261: Weak Encoding for Password
- CWE-322: Key Exchange without Entity Authentication
- CWE-323: Reusing a Nonce, Key Pair in Encryption
- CWE-324: Use of a Key Past its Expiration Date
- CWE-326: Inadequate Encryption Strength
- CWE-329: Generation of Predictable IV with CBC Mode
- CWE-347: Improper Verification of Cryptographic Signature
- CWE-640: Weak Password Recovery Mechanism for Forgotten Password

## SFP Primary Cluster: Malware (CWE-904)
- CWE-506: Embedded Malicious Code
- CWE-507: Trojan Horse
- CWE-508: Non-Replicating Malicious Code
- CWE-509: Replicating Malicious Code (Virus or Worm)
- CWE-510: Trapdoor
- CWE-511: Logic/Time Bomb
- CWE-512: Spyware
- CWE-69: Improper Handling of Windows ::DATA Alternate Data Stream
### SFP Secondary Cluster: Covert Channel (CWE-968)
- CWE-385: Covert Timing Channel
- CWE-514: Covert Channel
- CWE-515: Covert Storage Channel

## SFP Primary Cluster: Predictability (CWE-905)
- CWE-330: Use of Insufficiently Random Values
- CWE-331: Insufficient Entropy
- CWE-332: Insufficient Entropy in PRNG
- CWE-333: Improper Handling of Insufficient Entropy in TRNG
- CWE-334: Small Space of Random Values
- CWE-335: Incorrect Usage of Seeds in Pseudo-Random Number Generator (PRNG)
- CWE-336: Same Seed in Pseudo-Random Number Generator (PRNG)
- CWE-337: Predictable Seed in Pseudo-Random Number Generator (PRNG)
- CWE-338: Use of Cryptographically Weak Pseudo-Random Number Generator (PRNG)
- CWE-339: Small Seed Space in PRNG
- CWE-340: Generation of Predictable Numbers or Identifiers
- CWE-341: Predictable from Observable State
- CWE-342: Predictable Exact Value from Previous Values
- CWE-343: Predictable Value Range from Previous Values
- CWE-344: Use of Invariant Value in Dynamically Changing Context

## SFP Primary Cluster: UI (CWE-906)
### SFP Secondary Cluster: Feature (CWE-995)
- CWE-447: Unimplemented or Unsupported Feature in UI
- CWE-448: Obsolete Feature in UI
- CWE-449: The UI Performs the Wrong Action
- CWE-450: Multiple Interpretations of UI Input
- CWE-451: User Interface (UI) Misrepresentation of Critical Information
- CWE-549: Missing Password Field Masking
- CWE-655: Insufficient Psychological Acceptability
### SFP Secondary Cluster: Security (CWE-996)
- CWE-356: Product UI does not Warn User of Unsafe Actions
- CWE-357: Insufficient UI Warning of Dangerous Operations
- CWE-446: UI Discrepancy for Security Feature
### SFP Secondary Cluster: Information Loss (CWE-997)
- CWE-221: Information Loss or Omission
- CWE-222: Truncation of Security-relevant Information
- CWE-223: Omission of Security-relevant Information
- CWE-224: Obscured Security-relevant Information by Alternate Name

## SFP Primary Cluster: Other (CWE-907)
### SFP Secondary Cluster: Architecture (CWE-975)
- CWE-348: Use of Less Trusted Source
- CWE-359: Exposure of Private Personal Information to an Unauthorized Actor
- CWE-602: Client-Side Enforcement of Server-Side Security
- CWE-637: Unnecessary Complexity in Protection Mechanism (Not Using 'Economy of Mechanism')
- CWE-649: Reliance on Obfuscation or Encryption of Security-Relevant Inputs without Integrity Checking
- CWE-654: Reliance on a Single Factor in a Security Decision
- CWE-656: Reliance on Security Through Obscurity
- CWE-657: Violation of Secure Design Principles
- CWE-671: Lack of Administrator Control over Security
- CWE-693: Protection Mechanism Failure
- CWE-749: Exposed Dangerous Method or Function
### SFP Secondary Cluster: Compiler (CWE-976)
- CWE-733: Compiler Optimization Removal or Modification of Security-critical Code
### SFP Secondary Cluster: Design (CWE-977)
- CWE-115: Misinterpretation of Input
- CWE-187: Partial String Comparison
- CWE-188: Reliance on Data/Memory Layout
- CWE-193: Off-by-one Error
- CWE-349: Acceptance of Extraneous Untrusted Data With Trusted Data
- CWE-405: Asymmetric Resource Consumption (Amplification)
- CWE-406: Insufficient Control of Network Message Volume (Network Amplification)
- CWE-407: Inefficient Algorithmic Complexity
- CWE-408: Incorrect Behavior Order: Early Amplification
- CWE-409: Improper Handling of Highly Compressed Data (Data Amplification)
- CWE-410: Insufficient Resource Pool
- CWE-430: Deployment of Wrong Handler
- CWE-462: Duplicate Key in Associative List (Alist)
- CWE-463: Deletion of Data Structure Sentinel
- CWE-464: Addition of Data Structure Sentinel
- CWE-483: Incorrect Block Delimitation
- CWE-581: Object Model Violation: Just One of Equals and Hashcode Defined
- CWE-595: Comparison of Object References Instead of Object Contents
- CWE-618: Exposed Unsafe ActiveX Method
- CWE-648: Incorrect Use of Privileged APIs
- CWE-670: Always-Incorrect Control Flow Implementation
- CWE-682: Incorrect Calculation
- CWE-691: Insufficient Control Flow Management
- CWE-696: Incorrect Behavior Order
- CWE-697: Incorrect Comparison
- CWE-698: Execution After Redirect (EAR)
- CWE-705: Incorrect Control Flow Scoping
### SFP Secondary Cluster: Implementation (CWE-978)
- CWE-358: Improperly Implemented Security Check for Standard
- CWE-398: 7PK - Code Quality
- CWE-623: Unsafe ActiveX Control Marked Safe For Scripting
- CWE-710: Improper Adherence to Coding Standards

## SFP Primary Cluster: Faulty Resource Release (CWE-1237)
- CWE-415: Double Free
- CWE-762: Mismatched Memory Management Routines
- CWE-763: Release of Invalid Pointer or Reference

## SFP Primary Cluster: Failure to Release Memory (CWE-1238)
- CWE-401: Missing Release of Memory after Effective Lifetime

## Summary Statistics

| Metric | Count |
|---|---|
| SFP Primary Clusters | 23 |
| SFP Secondary Clusters | 57 |
| Individual member CWE weaknesses | 619 |

Primary clusters with no secondary clusters (members attach directly): Unused entities (CWE-886), Privilege (CWE-901), Malware (CWE-904, plus one secondary cluster Covert Channel), Predictability (CWE-905), Faulty Resource Release (CWE-1237), Failure to Release Memory (CWE-1238).

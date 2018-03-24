//
//  AppDelegate.m
//  PythonistaAppTemplate
//
//  Created by Ole Zorn on 15/02/16.
//  Copyright © 2016 omz-software. All rights reserved.
//

#import "PAAppDelegate.h"
#import "PAAppViewController.h"

#define checkPointsProductID @"com.mapman.checkpoints"

@interface PAAppDelegate () <UIGestureRecognizerDelegate, SKProductsRequestDelegate,SKPaymentTransactionObserver>

@end

static PAAppDelegate *PAAppDelegateInstance = nil;

@implementation PAAppDelegate

SKProductsRequest *productsRequest;
NSArray *validProducts;

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{
    
    PAAppDelegateInstance = self;
    
    [PAAppDelegate deleteProductsFile];
    
	NSString *scriptPath = [self copyScriptResourcesIfNeeded];
	
	self.window = [[UIWindow alloc] initWithFrame:[[UIScreen mainScreen] bounds]];
	self.window.rootViewController = [[PAAppViewController alloc] initWithScriptPath:scriptPath];
	[self.window makeKeyAndVisible];
	
	//This gesture recognizer suppresses the two-finger swipe-down gesture that can be used to dismiss
	//ui views without title bar in the main app. In a standalone app, this behavior is usually not desirable.
	UISwipeGestureRecognizer *swipeRecognizer = [[UISwipeGestureRecognizer alloc] initWithTarget:nil action:nil];
	swipeRecognizer.numberOfTouchesRequired = 2;
	swipeRecognizer.direction = UISwipeGestureRecognizerDirectionDown;
	swipeRecognizer.delegate = self;
	[self.window addGestureRecognizer:swipeRecognizer];
	
    [[UIApplication sharedApplication] setIdleTimerDisabled:YES];
    
	//This is required for the ui module to work correctly:
	[[PAEExtensionContext sharedContext] setApp:application];
	[[PAEExtensionContext sharedContext] setRootViewController:self.window.rootViewController];
	
	//Run the main script:
	if (scriptPath) {
		NSString *script = [NSString stringWithContentsOfFile:scriptPath encoding:NSUTF8StringEncoding error:NULL];
		if (script) {
			[[PythonInterpreter sharedInterpreter] run:script asFile:scriptPath];
		} else {
			NSLog(@"Could not load main.py (make sure its encoding is UTF-8)");
		}
	} else {
		NSLog(@"Could not find main.py");
	}
    
    [self fetchAvailableProducts];
    
	return YES;
    
}

- (NSString *)copyScriptResourcesIfNeeded
{
	//Copy files from <Main Bundle>/Scripts to ~/Library/Application Support/PythonistaScript.
	//Files that are already there (and up-to-date) are skipped.
	
	//The script is not run directly from the main bundle because its directory wouldn't be writable then,
	//which would require changes in scripts that produce files.
	NSString *bundledScriptDirectory = [[[NSBundle mainBundle] resourcePath] stringByAppendingPathComponent:@"Script"];
	NSString *appSupportDirectory = [NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory, NSUserDomainMask, YES) firstObject];
	NSString *writableScriptDirectory = [appSupportDirectory stringByAppendingPathComponent:@"PythonistaScript"];
	NSFileManager *fm = [NSFileManager defaultManager];
	[fm createDirectoryAtPath:writableScriptDirectory withIntermediateDirectories:YES attributes:nil error:NULL];
	
    #if TARGET_IPHONE_SIMULATOR
        NSString *mode = @"Simulator";
    #else
        NSString *mode = @"Device";
    #endif
    
	NSArray *scriptResources = [fm contentsOfDirectoryAtPath:bundledScriptDirectory error:NULL];

    BOOL has_error = NO;

	for (NSString *filename in scriptResources) {
        
        if (![filename isEqualToString:@"simulate_tilt.txt"] || [mode isEqualToString:@"Simulator"])
        {
        
            NSString *fullPath = [bundledScriptDirectory stringByAppendingPathComponent:filename];
            NSString *destPath = [writableScriptDirectory stringByAppendingPathComponent:filename];
            
            NSDate *srcModificationDate = [[fm attributesOfItemAtPath:fullPath error:NULL] fileModificationDate];
            NSDate *destModificationDate = [[fm attributesOfItemAtPath:destPath error:NULL] fileModificationDate];
            
            if (![destModificationDate isEqual:srcModificationDate] || [destModificationDate isEqual:NULL]) {
                
                [fm removeItemAtPath:destPath error:NULL];
                BOOL success = [fm copyItemAtPath:fullPath toPath:destPath error:NULL];
                
                if (!success)
                {
                    has_error = YES;
                }
                
            }

            
        }
        
	}
    
    NSString *mainScriptFile;
    
    if (!has_error)
    {
        mainScriptFile = [writableScriptDirectory stringByAppendingPathComponent:@"main.py"];
    }
    else
    {
        mainScriptFile = [writableScriptDirectory stringByAppendingPathComponent:@"copy_failed.py"];
    }
    
	return mainScriptFile;
}

- (BOOL)gestureRecognizer:(UIGestureRecognizer *)gestureRecognizer shouldBeRequiredToFailByGestureRecognizer:(UIGestureRecognizer *)otherGestureRecognizer
{
	if ([otherGestureRecognizer isKindOfClass:[UISwipeGestureRecognizer class]]) {
		UISwipeGestureRecognizer *otherSwipeRecognizer = (UISwipeGestureRecognizer *)otherGestureRecognizer;
		if (otherSwipeRecognizer.numberOfTouchesRequired == 2 && otherSwipeRecognizer.direction == UISwipeGestureRecognizerDirectionDown) {
			return YES;
		}
	}
	return NO;
}

- (BOOL)canMakePurchases {
    return [SKPaymentQueue canMakePayments];
}

+(void)fetchProducts
{
    if (PAAppDelegateInstance != nil)
    {
    [PAAppDelegateInstance fetchAvailableProducts];
    }
}

+(void)purchase
{
    if (PAAppDelegateInstance != nil)
    {
        [PAAppDelegateInstance fetchAvailableProducts];
    }
}
    
+(void)deleteProductsFile
{
    NSString *appSupportDirectory = [NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory, NSUserDomainMask, YES) firstObject];
    NSString *writableScriptDirectory = [appSupportDirectory stringByAppendingPathComponent:@"PythonistaScript"];
    NSString *destPath = [writableScriptDirectory stringByAppendingPathComponent:@"products.txt"];
    
    NSError *error;
    [[NSFileManager defaultManager] removeItemAtPath:destPath error:&error];
    
}

-(void)purchaseProduct
{
/*
    SKPayment *payment = [SKPayment paymentWithProduct:product];
    [[SKPaymentQueue defaultQueue] addTransactionObserver:self];
    [[SKPaymentQueue defaultQueue] addPayment:payment];
    
    @on_main_thread
    def purchase(self, product_identifier):
    
    if not self.can_make_purchases:
        raise Exception('Purchases are disabled')
        else:
            product = self.get_valid_product(product_identifier)
            sk_payment_class = ObjCClass("SKPayment")
            payment = sk_payment_class.alloc().init(product=product)
            default_queue = ObjCClass("SKPaymentQueue").defaultQueue
            default_queue.addTransactionObserver(self.purchase_controller)
            default_queue.addPayment(sk_payment_queue_class)
 */

}

-(void)fetchAvailableProducts
{
    
    NSSet *productIdentifiers = [NSSet
                                 setWithObjects:checkPointsProductID,nil];
    
    productsRequest = [[SKProductsRequest alloc]
                       initWithProductIdentifiers:productIdentifiers];
    
    productsRequest.delegate = self;
    
    [productsRequest start];
    
}

#pragma mark StoreKit Delegate

-(void)paymentQueue:(SKPaymentQueue *)queue
updatedTransactions:(NSArray *)transactions {
    for (SKPaymentTransaction *transaction in transactions) {
        switch (transaction.transactionState) {
            case SKPaymentTransactionStatePurchasing:
                NSLog(@"Purchasing");
                break;
                
            case SKPaymentTransactionStatePurchased:
                if ([transaction.payment.productIdentifier
                     isEqualToString:checkPointsProductID]) {
                    NSLog(@"Purchased ");
                    UIAlertView *alertView = [[UIAlertView alloc]initWithTitle:
                                              @"Purchase is completed succesfully" message:nil delegate:
                                              self cancelButtonTitle:@"Ok" otherButtonTitles: nil];
                    [alertView show];
                }
                [[SKPaymentQueue defaultQueue] finishTransaction:transaction];
                break;
                
            case SKPaymentTransactionStateRestored:
                NSLog(@"Restored ");
                [[SKPaymentQueue defaultQueue] finishTransaction:transaction];
                break;
                
            case SKPaymentTransactionStateFailed:
                NSLog(@"Purchase failed ");
                break;
            default:
                break;
        }
    }
}

-(void)productsRequest:(SKProductsRequest *)request
    didReceiveResponse:(SKProductsResponse *)response {

    SKProduct *validProduct = nil;

    if ([response.products count]>0) {
        
        /* https://developer.apple.com/documentation/storekit/skproduct */
        validProduct = [response.products objectAtIndex:0];
        
        if ([validProduct.productIdentifier
             isEqualToString:checkPointsProductID]){
            
            [PAAppDelegate deleteProductsFile];
            
            NSString *appSupportDirectory = [NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory, NSUserDomainMask, YES) firstObject];
            NSString *writableScriptDirectory = [appSupportDirectory stringByAppendingPathComponent:@"PythonistaScript"];
            NSString *destPath = [writableScriptDirectory stringByAppendingPathComponent:@".products"];
            
            [[NSFileManager defaultManager] createFileAtPath:destPath contents:nil attributes:nil];
            
            NSString *price_string = [NSString stringWithFormat:@"%@", validProduct.price];
            
            NSString *out_string = [NSString stringWithFormat:@"%1$@,%2$@",validProduct.productIdentifier, price_string];
            
            [out_string writeToFile:destPath atomically:YES encoding:NSUTF8StringEncoding error:nil];

        }
    }
    
}

@end

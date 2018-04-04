//
//  AppDelegate.m
//  PythonistaAppTemplate
//
//  Created by Ole Zorn on 15/02/16.
//  Copyright © 2016 omz-software. All rights reserved.
//

#import "PAAppDelegate.h"
#import "PAAppViewController.h"

#define checkPointsProductID @"com.mapmangame.checkpoints"

@interface PAAppDelegate () <UIGestureRecognizerDelegate, SKProductsRequestDelegate,SKPaymentTransactionObserver>

@end

static PAAppDelegate *PAAppDelegateInstance = nil;

@implementation PAAppDelegate

SKProductsRequest *productsRequest;
NSArray *validProducts;

PurchaseCallBack *purchaseCallBack;
ProductsCallBack *productsCallBack;
NSString *activeRestoreProductID;

- (void)applicationWillTerminate:(NSNotification *)notification
{
    [[SKPaymentQueue defaultQueue] removeTransactionObserver:self];
}

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{
    
    purchaseCallBack = nil;
    productsCallBack = nil;

    PAAppDelegateInstance = self;
    
    [PAAppDelegate deleteProductsFile];

    [[SKPaymentQueue defaultQueue] addTransactionObserver:self];
    
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
    
    /*[self fetchAvailableProducts];*/
    
	return YES;
    
}

-(NSString *)lastVersionFile;
{
    NSString *writableScriptDirectory = [PAAppDelegate getWritableScriptDirectory];
    NSString *fileName = @".last_version";
    NSString *destPath = [writableScriptDirectory stringByAppendingPathComponent:fileName];
    return destPath;
}

-(void)registerVersion:(NSString *) version;
{
    NSString *destPath = [self lastVersionFile];
    [version writeToFile:destPath atomically:YES encoding:NSUTF8StringEncoding error:nil];
}

-(NSString *)getLastVersion;
{
    
    NSFileManager *fileManager = [NSFileManager defaultManager];
    NSString *source = [self lastVersionFile];
    
    if ([fileManager fileExistsAtPath:source]){
        NSString *content = [NSString stringWithContentsOfFile:source encoding:NSUTF8StringEncoding error:nil];
        return content;
    }
    else{
        return @"NONE";
    }

}

-(NSString *)getCurrentVersion;
{
    NSDictionary *infoDictionary = [[NSBundle mainBundle]infoDictionary];
    NSString *version = infoDictionary[@"CFBundleShortVersionString"];
    NSString *build = infoDictionary[@"CFBundleVersion"];
    NSString *full_version = [NSString stringWithFormat:@"%@.%@", version, build];
    return full_version;
}

- (NSString *)copyScriptResourcesIfNeeded
{
    
#if TARGET_IPHONE_SIMULATOR
    NSString *mode = @"Simulator";
#else
    NSString *mode = @"Device";
#endif
    
    NSString *last_version = [self getLastVersion];
    NSString *current_version = [self getCurrentVersion];
    
    BOOL force_update_for_simulator = YES;
    BOOL up_to_date;

    if ([mode isEqualToString:@"Simulator"] && force_update_for_simulator)
    {
        up_to_date = NO;
    }
    else
    {
        if ([last_version isEqual:current_version])
        {
            up_to_date = YES;
            NSLog(@"Files up to date");
        }
        else
        {
            up_to_date = NO;
            NSLog(@"Files need updating");
        }
    }
        
	//Copy files from <Main Bundle>/Scripts to ~/Library/Application Support/PythonistaScript.
	//Files that are already there (and up-to-date) are skipped.
	
	//The script is not run directly from the main bundle because its directory wouldn't be writable then,
	//which would require changes in scripts that produce files.
	NSString *bundledScriptDirectory = [[[NSBundle mainBundle] resourcePath] stringByAppendingPathComponent:@"Script"];
	NSString *writableScriptDirectory = [PAAppDelegate getWritableScriptDirectory];

    NSFileManager *fm = [NSFileManager defaultManager];
	[fm createDirectoryAtPath:writableScriptDirectory withIntermediateDirectories:YES attributes:nil error:NULL];
    
	NSArray *scriptResources = [fm contentsOfDirectoryAtPath:bundledScriptDirectory error:NULL];

    BOOL has_error = NO;

    if (!up_to_date)
    {
        
        NSLog(@"Updating files");
        
        for (NSString *filename in scriptResources) {
            
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
    else
    {
        NSLog(@"Skipping file update");
    }
    
    NSString *mainScriptFile;
    
    if (!has_error)
    {
        
        [self registerVersion:current_version];
        
        if ([mode isEqualToString:@"Simulator"])
        {
            mainScriptFile = [writableScriptDirectory stringByAppendingPathComponent:@"main_simulate_tilt.py"];
        }
        else
        {
            mainScriptFile = [writableScriptDirectory stringByAppendingPathComponent:@"main.py"];
        }
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

+ (BOOL)canMakePayments {
    return [SKPaymentQueue canMakePayments];
}

+(NSSet *)getProductIdentifiers
{
    
    NSSet *productIdentifiers = [NSSet
                                 setWithObjects:checkPointsProductID,nil];
    
    return productIdentifiers;
    
}

+(void)fetchProducts:(ProductsCallBack *) callBack dummy:(NSString *)dummy;
{
    if (PAAppDelegateInstance != nil)
    {
        [PAAppDelegateInstance fetchAvailableProducts:callBack];
    }
}

+(void)purchase:(NSString *) productIdentifier callBack:(PurchaseCallBack *) callBack;
{
    if (PAAppDelegateInstance != nil)
    {
        [PAAppDelegateInstance purchaseProduct:productIdentifier callBack:callBack];
    }
}

+(void)restore:(NSString *) productIdentifier callBack:(PurchaseCallBack *) callBack;
{
    if (PAAppDelegateInstance != nil)
    {
        [PAAppDelegateInstance restoreProduct:productIdentifier callBack:callBack];
    }
}

+(void)deleteProductsFile
{

    NSString *destPath = [PAAppDelegate getProductsFile];
    
    NSError *error;
    [[NSFileManager defaultManager] removeItemAtPath:destPath error:&error];
    
}

+(NSString *)getProductsFile
{
    NSString *writableScriptDirectory = [PAAppDelegate getWritableScriptDirectory];
    NSString *destPath = [writableScriptDirectory stringByAppendingPathComponent:@".products"];
    return destPath;
}

+(NSString *)getWritableScriptDirectory
{
    NSString *appSupportDirectory = [NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory, NSUserDomainMask, YES) firstObject];
    NSString *writableScriptDirectory = [appSupportDirectory stringByAppendingPathComponent:@"PythonistaScript"];
    return writableScriptDirectory;
}

+(void)registerProduct:(NSString *) productIdentifier;
{
    NSString *writableScriptDirectory = [PAAppDelegate getWritableScriptDirectory];
    NSString *fileName = [NSString stringWithFormat:@".%1$@",productIdentifier];
    NSString *destPath = [writableScriptDirectory stringByAppendingPathComponent:fileName];
    [productIdentifier writeToFile:destPath atomically:YES encoding:NSUTF8StringEncoding error:nil];
}

-(void)purchaseProduct:(NSString *)productIdentifier callBack:(PurchaseCallBack *) callBack;
{
    
    SKProduct *product = [self getProduct:productIdentifier];

    if (product != nil)
    {
        purchaseCallBack = callBack;
        SKPayment *payment = [SKPayment paymentWithProduct:product];
        [[SKPaymentQueue defaultQueue] addPayment:payment];
    }else{
        purchaseCallBack = nil;
    }
    
}

-(void)restoreProduct:(NSString *)productIdentifier callBack:(PurchaseCallBack *) callBack;
{
    
    SKProduct *product = [self getProduct:productIdentifier];
    
    if (product != nil)
    {
        purchaseCallBack = callBack;
        activeRestoreProductID = productIdentifier;
        [[SKPaymentQueue defaultQueue] restoreCompletedTransactions];
    }else{
        purchaseCallBack = nil;
    }
    
}

-(void)fetchAvailableProducts:(ProductsCallBack *) callBack;
{
    
    productsCallBack = callBack;
    
    NSSet *productIdentifiers = [PAAppDelegate getProductIdentifiers];
    
    productsRequest = [[SKProductsRequest alloc]
                       initWithProductIdentifiers:productIdentifiers];
    
    productsRequest.delegate = self;
    
    [productsRequest start];
    
}

-(SKProduct *)getProduct:(NSString *)productIdentifier
{
    
    int i;
    SKProduct *validProduct = nil;
    
    for (i=0;i<validProducts.count>0;i++)
    {
        validProduct = [validProducts objectAtIndex:i];
        if ([validProduct.productIdentifier
             isEqualToString:productIdentifier]){
            return validProduct;
        }
    }
    
    return nil;
    
}

#pragma mark StoreKit Delegate

- (void)paymentQueue:(SKPaymentQueue *)queue restoreCompletedTransactionsFailedWithError:(NSError *)error{
    
    if (purchaseCallBack != nil)
    {
        NSString *error_message = error.localizedDescription;
        [purchaseCallBack failed:activeRestoreProductID error:error_message];
    }
    
}

//Then this delegate Function Will be fired
- (void) paymentQueueRestoreCompletedTransactionsFinished:(SKPaymentQueue *)queue
{
    for (SKPaymentTransaction *transaction in queue.transactions)
    {
        
        NSString *productIdentifier = transaction.payment.productIdentifier;
        
        NSLog(@"Restored ");
        
        [PAAppDelegate registerProduct:productIdentifier];
        
        [[SKPaymentQueue defaultQueue] finishTransaction:transaction];
        
        if (purchaseCallBack != nil)
        {
            [purchaseCallBack restored:productIdentifier dummy:productIdentifier];
        }
        
    }
}

-(void)paymentQueue:(SKPaymentQueue *)queue
updatedTransactions:(NSArray *)transactions {
    for (SKPaymentTransaction *transaction in transactions) {
        
        NSString *productIdentifier = transaction.payment.productIdentifier;
        
        switch (transaction.transactionState) {
            case SKPaymentTransactionStatePurchasing:
                
                NSLog(@"Purchasing");
                
                if (purchaseCallBack != nil)
                {
                    [purchaseCallBack inProgress:productIdentifier dummy:productIdentifier];
                }
                
                break;
                
            case SKPaymentTransactionStatePurchased:
                
                NSLog(@"Purchased ");
                
                [PAAppDelegate registerProduct:transaction.payment.productIdentifier];
                
                if (purchaseCallBack != nil)
                {
                    [purchaseCallBack successful:productIdentifier dummy:productIdentifier];
                }
                
                [[SKPaymentQueue defaultQueue] finishTransaction:transaction];
                break;
                
            case SKPaymentTransactionStateRestored:
                
                NSLog(@"Restored ");
                
                [PAAppDelegate registerProduct:productIdentifier];
                
                [[SKPaymentQueue defaultQueue] finishTransaction:transaction];
                if (purchaseCallBack != nil)
                {
                    [purchaseCallBack restored:productIdentifier dummy:productIdentifier];
                }
                
                break;
                
            case SKPaymentTransactionStateFailed:
                
                NSLog(@"Purchase failed ");
                /*
                 0 : Cannot connect to iTunes Store
                 */
                /*
                NSLog([NSString stringWithFormat:@"%ld", transaction.error.code]);
                NSLog(transaction.error.localizedDescription);
                */
                [[SKPaymentQueue defaultQueue] finishTransaction:transaction];
                if (purchaseCallBack != nil)
                {
                    NSString *error = transaction.error.localizedDescription;
                    [purchaseCallBack failed:productIdentifier error:error];
                }
                
                break;
            
            case SKPaymentTransactionStateDeferred:

                NSLog(@"Deferred ");
                
                if (purchaseCallBack != nil)
                {
                    [purchaseCallBack deferred:productIdentifier dummy:productIdentifier];
                }
                
                break;
                
            default:
                break;
        }
    }
}

-(void)productsRequest:(SKProductsRequest *)request
    didReceiveResponse:(SKProductsResponse *)response {

    validProducts = response.products;

    SKProduct *validProduct = nil;
    NSMutableString *content;
    int i;

    [PAAppDelegate deleteProductsFile];

    if (validProducts.count > 0)
    {
        NSLog(@"Products Received");
        
        NSString *destPath = [PAAppDelegate getProductsFile];
        
        [[NSFileManager defaultManager] createFileAtPath:destPath contents:nil attributes:nil];

        content = [[NSMutableString alloc] init];
        
        for (i=0;i<validProducts.count>0;i++) {
            
            /* https://developer.apple.com/documentation/storekit/skproduct */
            validProduct = [validProducts objectAtIndex:i];
            
            NSString *price_string = [NSString stringWithFormat:@"%@", validProduct.price];
            
            NSString *out_string = [NSString stringWithFormat:@"%1$@,%2$@",validProduct.productIdentifier, price_string];
            
            [content appendFormat: @"%@\n", out_string];

        }
        
        [content writeToFile:destPath atomically:YES encoding:NSUTF8StringEncoding error:nil];
    
    }
    else
    {
        NSLog(@"No Products Received");
    }

    if (productsCallBack != nil)
    {
        [productsCallBack loaded];
    }
    
}

@end

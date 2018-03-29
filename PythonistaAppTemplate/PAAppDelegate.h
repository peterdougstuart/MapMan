//
//  AppDelegate.h
//  PythonistaAppTemplate
//
//  Created by Ole Zorn on 15/02/16.
//  Copyright © 2016 omz-software. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <StoreKit/StoreKit.h>

@interface PAAppDelegate : UIResponder <UIApplicationDelegate>

@property (strong, nonatomic) UIWindow *window;



@end

@interface PythonInterpreter : NSObject

+ (id)sharedInterpreter;
- (void)run:(NSString *)script asFile:(NSString *)scriptPath;

@end

@interface PAEExtensionContext : NSObject

@property (retain) UIViewController *rootViewController;
@property (retain) UIApplication *app;
+ (instancetype)sharedContext;

@end

@interface PurchaseCallBack : NSObject

- (void)successful:(NSString *)identifier dummy:(NSString *)dummy;
- (void)failed:(NSString *)identifier error:(NSString *)error;
- (void)restored:(NSString *)identifier dummy:(NSString *)dummy;
- (void)inProgress:(NSString *)identifier dummy:(NSString *)dummy;

@end

@interface ProductsCallBack : NSObject

- (void)loaded;

@end
